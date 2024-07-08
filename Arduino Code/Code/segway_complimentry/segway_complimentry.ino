/******************************************************************************************************************
Segway Balancing Code
By: Vishwas Gajera, Tanay Srinivasa

Functions Called in Setup and Loop are Defined in func.ino:
        - void read_imu()                : Reads roll and pitch from MPU6050 Through Wire
        - void calculate_IMU_error()     : Used to Calibrate MPU6050

**** Encoder Pins ****
Pin 1 - 2
Pin 2 - 3

**** Motor Pins ****
dir_pin 7
pwm_pin 6

**** IMU Pins ****
SCL - A4
SDA - A5
******************************************************************************************************************/

#include <Wire.h>
#include <Encoder.h>
#include <TrivikramEncoder.h>

/* MPU Initialization*/
const int MPU = 0x68; // MPU6050 I2C address
float AccX, AccY, AccZ;
float GyroX, GyroY, GyroZ;
float accAngleX, accAngleY, gyroAngleX, gyroAngleY, gyroAngleZ;
float roll, pitch, yaw;
float AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ;
float elapsedTime, currentTime, previousTime;
float t,lastt,dt;
float looptime_print;
int c = 0;   //counter for imu error calculation

/* Loop Time Definition */
float LoopTimer;

/* Encoder Parameters */
#define wheelMotorPPR 2264/4
#define pi 3.141592

//these pins can not be changed 2/3 are special pins (Interrupt Capable)
#define encoderPin1 2
#define encoderPin2 3
Encoder wheelEnc(encoderPin1, encoderPin2);

volatile int lastEncoded = 0;
volatile long encoderValue = 0;
volatile long encoder_x=0;

long lastencoderValue = 0;

int lastMSB = 0;
int lastLSB = 0;

// Deadband for Motor Inputs //
float deadzone=0;

/* PID Setup */

// Offsets For Balance Position //
float target_roll=+2;
float target_enc=0;

// Error Initialisation //
float error_roll=0;
float last_error_roll=0;
float error_enc=0;
float last_error_enc=0;

/* PID Setup */

// Gains for Roll //
float Kp=14;//5;//16;           // theta gain
float Kd=0.1;//1.2;//1.5;      // theta dot gain
float Ki=100;

// Gains for Encoder //
float Kp2=0;                  // x gain
float Kd2=3;//4.5;            // x_dot gain

// Error Function Initialisation //
float u=0;
float u1=0;
float u2=0;
float u3=0;
float u4=0;
float u5=0;

// PWM Value Initialisation //
float pwm=0;

// Sign of Roll and Previous Roll for Integral Wind-Up //
int sgnRoll, sgnPrevRoll;

/* Motor Pin Definition */
#define dir_pin 7
#define pwm_pin 6

void setup() {
        Serial.begin(19200);

        pinMode(13, OUTPUT);
        digitalWrite(13, HIGH);

        Wire.begin();                      // Initialize comunication
        Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
        Wire.write(0x6B);                  // Talk to the register 6B
        Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
        Wire.endTransmission(true);        //end the transmission

        pinMode(encoderPin1, INPUT_PULLUP);
        pinMode(encoderPin2, INPUT_PULLUP);
        delay(20);

        sgnRoll = 0;
        sgnPrevRoll = 0;
}

void loop() {
        read_imu();
        sgnRoll = (roll > 0)? 1 : -1;
        
        // Serial.print("Roll: "); 
        // Serial.println(roll,5);
        lastt=t;
        t=micros();
        dt=(t-lastt)/1000000;
        //Serial.println(dt,6);

        encoderValue = wheelEnc.read();
        // Serial.print("encoderValue: "); Serial.println(encoderValue);

        error_roll = target_roll-roll;
        error_enc = (target_enc - (encoderValue/8530.0))*2*pi;   //8530 encoder constant 8530 interupts per round //
        // Serial.print("error_enc: "); Serial.println(error_enc);

        if (fabs(error_roll) < deadzone ){
                u=0;
                pwm=fabs(u);
        } else {
                // Error Function Calculation //
                u1 = Kp*error_roll;
                u2=-Kd*GyroX;
                u3 += Ki*(error_roll)*dt;
                u3 = constrain(u3,-20,20);
                u4 = Kp2*error_enc;
                u5 = Kd2*(error_enc-last_error_enc)/dt;

                last_error_roll=error_roll;
                last_error_enc=error_enc;

                u=u1+u2+u3+u4+u5;
                pwm=fabs(u);
                if (pwm > 255) pwm=255;
        }

        if (fabs(roll)>20) pwm=0;

        // Printing Individual Controllers //
        Serial.print(u1); Serial.print(" ");
        Serial.print(u2); Serial.print(" ");
        Serial.print(u3); Serial.print(" ");
        Serial.print(u4); Serial.print(" ");
        Serial.print(u5); Serial.print(" ");
        Serial.println("");

        if (micros() - LoopTimer > 3000){
                digitalWrite(dir_pin, u <= 0.0 ? LOW : HIGH);
                analogWrite(pwm_pin,pwm);

                LoopTimer=micros();
        }

        // Integral Wind-Up //
        if (sgnRoll != sgnPrevRoll)
                u3 = 0;
        sgnPrevRoll = sgnRoll;
}