/*
   Encoder Method : http://makeatronics.blogspot.com/2013/02/efficiently-reading-quadrature-with.html
   Teensy Datasheet : https://www.pjrc.com/teensy/K66P144M180SF5RMV2.pdf
   pg 2189 for GPIO register data
   Teensy Interrupts Reference: https://www.pjrc.com/teensy/interrupts.html
   Teensy GPIO Register Mapping : https://forum.pjrc.com/archive/index.php/t-17532.html
   Motor Driver Tutorial: https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/
   PID library : https://playground.arduino.cc/Code/PIDLibrary/
   IMU datasheet  : https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
   IMU library    : https://github.com/ElectronicCats/mpu6050
   Teensy Wire library :

   This program uses the L298N motor driver to drive 2 motors, one tracking a velocity command and the other tracking a
   position command.  The PID algorithms use encoder data as feedback and were tuned using the Zieglers-Nichols Method first
   to get near the right numbers, then tuned heuristically afterwards.  The velocity and position commands switch sign every
   5 seconds to test for robustness (needs to turn in both directions).  As it stands, the motors saturate briefly while
   changing direction.

   Change around the pin definitions as needed.  Get the encoder GPIOX_DIR pin mapping from 'Teensy GPIO Register Mapping'.


   PID TUNING:
   Using the Zieglers-Nichols Method (for the right ballpark) ... https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method

   Velocity controller -
   Ku = 200, Tu = 0.16s (approximate)
   PI : Kp = 90, Ki = 675 -             settling time of about 1 second, works well
   PID : Kp = 120, Ki = 1500, Kd = 4 -  a little ringing upon switching directions, not suitable, need to decrease Kd
   PID : Kp = 120, Ki = 1500, Kd = 1 -  settling time << 1 second, no noticeable ringing, best iteration so far

   Position controller -
   Ku = 280, Tu = 0.52s (approximate)
   PID : Kp = 168, Ki = 646, Kd = 11 -  saturates quickly, lots of overshoot and ringing
   PD : Kp = 160, Kd = 13 -  a little ringing, but the best so far

   NOTE : THIS IS FOR UNLOADED MOTORS , CONTROLLERS WILL NEED TUNING AFTER BEING IMPLEMENTED IN THE ROBOT

   Robert Whitney : rw429@cornell.edu : October 2020
*/

#include <Streaming.h>
#include <MPU6050.h>
#include <Wire.h>
#include <PID_v1.h>

//L298N Control pin mapping on teensy (4 motors, 3 pins each, 12 total)
//IN1 and IN2 control direction of motor 1, EN1 controls speed of motor 1
//IN3 and IN4 control direction of motor 2, EN2 controls speed of motor 2
//#define IN1 4
//#define IN2 5
//#define IN3 10
//#define IN4 11
//#define EN1 6 //PWM
//#define EN2 9 //PWM

#define IN1 27
#define IN2 28
#define IN3 31
#define IN4 32
#define EN1 29 //PWM
#define EN2 30 //PWM

//Encoder interrupt pin mapping on teensy (4 encoders, 2 channels each, 8 total)
#define ENCD1_PINA 16 //GPIOB_PDIR, bits 0 & 1
#define ENCD1_PINB 17
#define ENCD2_PINA 19 //GPIOB_PDIR, bits 2 & 3
#define ENCD2_PINB 18

#define CntsPerRev    2160
#define Cnts2Rev      1/CntsPerRev
#define Pi            3.1415926
#define rad2deg       180/Pi
#define gyrLSB2Degs   1/65.5  //deg/(s*LSB) (for +/- 500 deg/s range)
#define accLSB2Gs     1/16384 //g/LSB       (for +/- 2g range, not really necessary if just calculating angles)


///////////////// Parameters /////////////////

//PID Velocity Controller
#define Kp_vel 110
#define Ki_vel 1100
#define Kd_vel 0

//PID Position Controller
#define Kp_pos 160
#define Ki_pos 15
#define Kd_pos 13

//IMU comp filter : increase alpha to trust gyro more, decrease to trust acc more
#define alphaP 0.99 //pitch
#define alphaR 0.99 //roll

//////////////////////////////////////////////


// Encoder Counts
volatile double cntEncd1 = 0, cntEncd2 = 0;

//Encoder state change lookup table
const int ENCODER_LOOKUP[] = {0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0};

// Encoder Structs, needs to be doubles for PID controller
struct ENCODER {
  double Vel = 0 , Pos = 0, lastCnt = 0;
};

ENCODER ENCD1, ENCD2;
elapsedMicros lastTime_ENCD;

//Motor pin mapping
const uint8_t MOTOR1[3] = {IN1, IN2, EN1}, MOTOR2[3] = {IN3, IN4, EN2};

//Encoder PID variables
double velRef = 0, vel = 0, velCmd = 0; //desired velocity [rev/s], current velocity [rev/s], command to motor 1
double posRef = 0, pos = 0, posCmd = 0; //desired position [rad], current position [rad], command to motor 2

//PID controllers for position and speed
PID ENCD1_PID(&pos, &posCmd, &posRef, Kp_pos, Ki_pos, Kd_pos, DIRECT);  //position control
PID ENCD2_PID(&vel, &velCmd, &velRef, Kp_vel, Ki_vel, Kd_vel, DIRECT);  //velocity control

//for demo
elapsedMillis changeDir;
bool spinForward = true;

//IMU
MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;

//initialized to zero
float rollComp = 0, pitchComp = 0;
elapsedMicros lastTime_IMU;


void setup() {

  Serial.begin(115200);   //Serial Monitor
  Serial1.begin(57600);   //Telemetry Radio

  //setup I2C bus using pins 7/8 (pins 18/19 used for encoder interrupts)
  Wire.begin();
  Wire.setSCL(7);
  Wire.setSDA(8);

  //L298N Control Pins for motors 1 and 2
  pinMode(IN1, OUTPUT);  pinMode(IN2, OUTPUT);  pinMode(EN1, OUTPUT);
  pinMode(IN3, OUTPUT);  pinMode(IN4, OUTPUT);  pinMode(EN2, OUTPUT);

  //Encoder interrupts
  attachInterrupt(ENCD1_PINA, ENCD1_ISR, CHANGE);
  attachInterrupt(ENCD1_PINB, ENCD1_ISR, CHANGE);
  attachInterrupt(ENCD2_PINA, ENCD2_ISR, CHANGE);
  attachInterrupt(ENCD2_PINB, ENCD2_ISR, CHANGE);

  //Constrain PID limits
  ENCD1_PID.SetOutputLimits(-255, 255);
  ENCD2_PID.SetOutputLimits(-255, 255);

  //Start PID Control
  ENCD1_PID.SetMode(AUTOMATIC);
  ENCD2_PID.SetMode(AUTOMATIC);

  velRef = 0.5; //rev/s
  posRef = Pi / 2;  //rad

  // initialize device & verify connection
  Serial.println("Initializing IMU...");
  accelgyro.initialize();
  Serial.println("Testing device connections...");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

  //set the correct scaling (+/- 2g acc, +/- 500deg/s gyro)
  accelgyro.setFullScaleGyroRange(MPU6050_GYRO_FS_500);
  accelgyro.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);

  // use the code below to change accel/gyro offset values
  accelgyro.setXAccelOffset(-1345);
  accelgyro.setYAccelOffset(-4063);
  accelgyro.setZAccelOffset(1779);
  accelgyro.setXGyroOffset(90);
  accelgyro.setYGyroOffset(5);
  accelgyro.setZGyroOffset(13);
}

void loop() {

        // Sense //
        getMotorSpeed();
        pos = ENCD1.Pos;
        vel = ENCD2.Vel;

        // read raw accel/gyro measurements from device [LSB] //
        accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

        // Compute //
        ENCD1_PID.Compute();
        ENCD2_PID.Compute();

        // check for saturation //
        int isSat = 0;
        if (abs(posCmd) == 255) isSat = 1;

        // Euler angles from accelerometer, will be noisy but stable //
        float rollAcc = atan2((float)ay , (float)az) * rad2deg;
        float pitchAcc = atan2((float) - ax , sqrt((float)ay * (float)ay + (float)az * (float)az)) * rad2deg;

        // Euler Angle Complementary Filter, stable and accurate //
        float dT = (float)lastTime_IMU / 1000000;
        lastTime_IMU = 0;
        rollComp = alphaR * (rollComp + (float)gx * dT * gyrLSB2Degs) + (1 - alphaR) * rollAcc;
        pitchComp = alphaP * (pitchComp + (float)gy * dT * gyrLSB2Degs) + (1 - alphaP) * pitchAcc;

        // Actuate //
        setMotor(MOTOR1, posCmd);
        setMotor(MOTOR2, velCmd);

        // Send Relevant Data Over Telemetry Radio (Serial1) //
        Serial1 << rollComp << "," << pitchComp << "," << pos << "," << posRef << "," << posCmd << "," << vel << "," << velRef << "," << velCmd << endl;
        Serial << posRef << "\t" << pos << "\t" << isSat << endl;
        delay(1);


        // For Demo : change setpoint every 4 seconds //
        if (changeDir > 4000) {
                changeDir = 0;
                if (spinForward) { // if we were spinning forward //
                        velRef = -velRef;
                        posRef = -posRef;
                        spinForward = !spinForward;
                }
                else {
                        velRef = -velRef;
                        posRef = -posRef;
                        spinForward = !spinForward;
                }
        }
}
