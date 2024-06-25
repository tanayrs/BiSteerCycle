
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
   GPS library : https://github.com/SlashDevin/NeoGPS

   This program is for testing all 4 motors on the actual prototype.  This is what I used to try to develop and tune the motor 
   controllers for bike ballet.  Download 'Demos->bikeBallet' for more information.

   Robert Whitney : rw429@cornell.edu : November 2020
*/

#include <Streaming.h>
#include <PID_v1.h>

//L298N Control pin mapping on teensy (4 motors, 3 pins each, 12 total)
//IN1 and IN2 control direction of motor 1, EN1 controls speed of motor 1
//IN3 and IN4 control direction of motor 2, EN2 controls speed of motor 2, etc
#define IN1 6
#define IN2 5
#define IN3 4
#define IN4 3
#define IN5 32
#define IN6 31
#define IN7 28
#define IN8 27
#define EN1 7   //PWM
#define EN2 2   //PWM
#define EN3 30  //PWM
#define EN4 29  //PWM

//Encoder interrupt pin mapping on teensy (4 encoders, 2 channels each, 8 total)
#define ENCD1_PINA 22 //GPIOC_PDIR, bits 1 & 2
#define ENCD1_PINB 23
#define ENCD2_PINA 11 //GPIOC_PDIR, bits 6 & 7
#define ENCD2_PINB 12
#define ENCD3_PINA 16 //GPIOB_PDIR, bits 0 & 1
#define ENCD3_PINB 17
#define ENCD4_PINA 19 //GPIOB_PDIR, bits 2 & 3
#define ENCD4_PINB 18

//useful constants
#define Pos_CntsPerRev    5100  //approximated
#define Pos_Cnts2Rev      1/Pos_CntsPerRev
#define Vel_CntsPerRev    1080  // 2160CPR/2 (for gearing ratio)
#define Vel_Cnts2Rev      1/Vel_CntsPerRev
#define Pi                3.1415926
#define rad2deg           180/Pi
#define gyrLSB2Dps        1/65.5  //deg/(s*LSB) (for +/- 500 deg/s range)
#define accLSB2Gs         1/16384 //g/LSB       (for +/- 2g range, not really necessary if just calculating angles)


///////////////// Parameters /////////////////

#define vel_LPF 0.5

//PID Velocity Controller
#define Kp_vel1 3
#define Ki_vel1 0
#define Kd_vel1 0

#define Kp_vel2 6
#define Ki_vel2 4
#define Kd_vel2 0

#define Kp_vel3 3
#define Ki_vel3 0
#define Kd_vel3 0

#define Kp_vel4 6
#define Ki_vel4 4
#define Kd_vel4 0

//PID Position Controllers
#define Kp_pos1 0.45
#define Ki_pos1 0.08
#define Kd_pos1 0

#define Kp_pos3 0.5
#define Ki_pos3 0.08
#define Kd_pos3 0

#define MOTOR1_DEADBAND 75
#define MOTOR2_DEADBAND 83
#define MOTOR3_DEADBAND 73
#define MOTOR4_DEADBAND 78

#define MOTOR1_FF 12
#define MOTOR2_FF 20
#define MOTOR3_FF 15
#define MOTOR4_FF 22

#define MOTOR1_WHEEL_REF_FF 2       //FF term for position motor 1 in response to the reference velocity of motor 2
#define MOTOR3_WHEEL_REF_FF 2


//Motor pin mappings
const uint8_t MOTOR1[4] = {IN1, IN2, EN1, MOTOR1_DEADBAND}, MOTOR2[4] = {IN3, IN4, EN2, MOTOR2_DEADBAND},
                          MOTOR3[4] = {IN5, IN6, EN3, MOTOR3_DEADBAND}, MOTOR4[4] = {IN7, IN8, EN4, MOTOR4_DEADBAND};

// Encoder Counts and state change lookup table
volatile double cntEncd1 = 0, cntEncd2 = 0, cntEncd3 = 0, cntEncd4 = 0;
const int ENCODER_LOOKUP[] = {0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0};

// Encoder Structs, needs to be doubles for PID controller
struct ENCODER {
  double Vel = 0 , Pos = 0, lastCnt = 0;
};

// 1 & 3 : Position, 2 & 4 : Velocity
ENCODER ENCD1, ENCD2, ENCD3, ENCD4;
elapsedMicros lastTime_ENCD;

//Encoder PID variables
double pos1_Ref = 0; //desired position [rad]
double pos3_Ref = 0;

double vel1_Ref = 0,    vel1_Cmd = 0;   //desired velocity from PID controller 1 [rev/s], command to motor 1 [LSB]
double vel2_Ref = 0.5, vel2_Cmd = 0;   //desired velocity [rev/s], command to motor 2 [LSB]
double vel3_Ref = 0,    vel3_Cmd = 0;
double vel4_Ref = 0.5, vel4_Cmd = 0;


//PID controllers for position and speed
PID ENCD1_PID_POS(&ENCD1.Pos, &vel1_Ref, &pos1_Ref, Kp_pos1, Ki_pos1, Kd_pos1, DIRECT);  //position control
PID ENCD3_PID_POS(&ENCD3.Pos, &vel3_Ref, &pos3_Ref, Kp_pos3, Ki_pos3, Kd_pos3, DIRECT);

PID ENCD1_PID_VEL(&ENCD1.Vel, &vel1_Cmd, &vel1_Ref, Kp_vel1, Ki_vel1, Kd_vel1, DIRECT);  //velocity control
PID ENCD2_PID_VEL(&ENCD2.Vel, &vel2_Cmd, &vel2_Ref, Kp_vel2, Ki_vel2, Kd_vel2, DIRECT);
PID ENCD3_PID_VEL(&ENCD3.Vel, &vel3_Cmd, &vel3_Ref, Kp_vel3, Ki_vel3, Kd_vel3, DIRECT);
PID ENCD4_PID_VEL(&ENCD4.Vel, &vel4_Cmd, &vel4_Ref, Kp_vel4, Ki_vel4, Kd_vel4, DIRECT);

elapsedMillis switchTime;



void setup() {

  Serial.begin(115200);   //Serial Monitor

  //L298N Control Pins for motors 1 and 2
  pinMode(IN1, OUTPUT);  pinMode(IN2, OUTPUT);  pinMode(EN1, OUTPUT);
  pinMode(IN3, OUTPUT);  pinMode(IN4, OUTPUT);  pinMode(EN2, OUTPUT);
  pinMode(IN5, OUTPUT);  pinMode(IN6, OUTPUT);  pinMode(EN3, OUTPUT);
  pinMode(IN7, OUTPUT);  pinMode(IN8, OUTPUT);  pinMode(EN4, OUTPUT);

  //Encoder interrupts
  attachInterrupt(ENCD1_PINA, ENCD1_ISR, CHANGE);
  attachInterrupt(ENCD1_PINB, ENCD1_ISR, CHANGE);
  attachInterrupt(ENCD2_PINA, ENCD2_ISR, CHANGE);
  attachInterrupt(ENCD2_PINB, ENCD2_ISR, CHANGE);
  attachInterrupt(ENCD3_PINA, ENCD3_ISR, CHANGE);
  attachInterrupt(ENCD3_PINB, ENCD3_ISR, CHANGE);
  attachInterrupt(ENCD4_PINA, ENCD4_ISR, CHANGE);
  attachInterrupt(ENCD4_PINB, ENCD4_ISR, CHANGE);

  //Constrain PID limits
  ENCD1_PID_POS.SetOutputLimits(-10 * Pi, 10 * Pi); //rad
  ENCD3_PID_POS.SetOutputLimits(-10 * Pi, 10 * Pi);

  ENCD1_PID_VEL.SetOutputLimits(MOTOR1_DEADBAND - 255, 255 - MOTOR1_DEADBAND);  //LSB
  ENCD2_PID_VEL.SetOutputLimits(MOTOR2_DEADBAND - 255, 255 - MOTOR2_DEADBAND);
  ENCD3_PID_VEL.SetOutputLimits(MOTOR3_DEADBAND - 255, 255 - MOTOR3_DEADBAND);
  ENCD4_PID_VEL.SetOutputLimits(MOTOR4_DEADBAND - 255, 255 - MOTOR4_DEADBAND);


  //Start PID Control
  ENCD1_PID_POS.SetMode(AUTOMATIC);
  ENCD3_PID_POS.SetMode(AUTOMATIC);

  ENCD1_PID_VEL.SetMode(AUTOMATIC);
  ENCD2_PID_VEL.SetMode(AUTOMATIC);
  ENCD3_PID_VEL.SetMode(AUTOMATIC);
  ENCD4_PID_VEL.SetMode(AUTOMATIC);

}

void loop() {


  //////// Sense ////////
  getMotorData();


  //////// Compute ////////
  //Update encoder PIDs
  ENCD1_PID_POS.Compute();
  ENCD3_PID_POS.Compute();

  ENCD1_PID_VEL.Compute();
  ENCD2_PID_VEL.Compute();
  ENCD3_PID_VEL.Compute();
  ENCD4_PID_VEL.Compute();


  //////// Actuate ////////
  double uM1 = vel1_Cmd + sign(vel1_Ref) * sq(vel1_Ref * MOTOR1_FF) - vel2_Ref * MOTOR1_WHEEL_REF_FF;
  double uM2 = vel2_Cmd + vel2_Ref * MOTOR2_FF;
  double uM3 = vel3_Cmd + sign(vel3_Ref) * sq(vel3_Ref * MOTOR3_FF) - vel4_Ref * MOTOR3_WHEEL_REF_FF;
  double uM4 = vel4_Cmd + vel4_Ref * MOTOR4_FF;

  setMotor(MOTOR1, uM1);
  setMotor(MOTOR2, uM2);
  setMotor(MOTOR3, uM3);
  setMotor(MOTOR4, uM4);

  bool isSat1 = false, isSat2 = false, isSat3 = false, isSat4 = false;
  if (abs(uM1) + MOTOR1_DEADBAND >= 255) isSat1 = true;
  if (abs(uM2) + MOTOR2_DEADBAND >= 255) isSat2 = true;
  if (abs(uM3) + MOTOR3_DEADBAND >= 255) isSat3 = true;
  if (abs(uM4) + MOTOR4_DEADBAND >= 255) isSat4 = true;

  //  Serial << ENCD1.Pos << "\t" << isSat1 << "\t" << pos1_Ref << "\t" << ENCD1.Vel << "\t" << vel1_Ref << "\t"  << endl;
  Serial << ENCD2.Vel << "\t" << isSat2 << "\t" << vel2_Ref << endl;
  //    Serial << ENCD2.Vel << "\t" << isSat2 << "\t" << vel2_Ref << endl;
  //  Serial << abs(vel2_Cmd + vel2_Ref * MOTOR2_FF) + MOTOR2_DEADBAND << endl;
  //  Serial << ENCD3.Pos << "\t" << isSat3 << "\t" << pos3_Ref << "\t" << ENCD3.Vel << "\t" << vel3_Ref << "\t"  << endl;
  //    Serial << ENCD2.Vel << "\t" << isSat2 << "\t" << vel2_Ref << endl;
  delay(10);

  if (switchTime > 2000) {
    switchTime = 0;
    pos1_Ref = -pos1_Ref;
    vel2_Ref = -vel2_Ref;
    pos3_Ref = -pos3_Ref;
    vel4_Ref = -vel4_Ref;
  }

}
