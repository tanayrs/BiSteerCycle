#include <Wire.h>
#include <Encoder.h>
#include <TrivikramEncoder.h>
#include <CytronMotorDriver.h>

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
CytronMD wheelMotor(PWM_DIR, 6, 8);

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
float target_roll=0;
float target_enc=0;
float roll_offset=4.4;

// Error Initialisation //
float error_roll=0;
float last_error_roll=0;
float error_enc=0;
float last_error_enc=0;

/* PID Setup */

// Gains for Roll //
float Kp=25;//5;//16;           // theta gain
float Kd=0;//1.2;//1.5;      // theta dot gain
float Ki=5;

// Gains for Encoder //
float Kd_wheel=0;//4.5;            // x_dot gain

// Error Function Initialisation //
float u=0;
float int_lean=0;

// PWM Value Initialisation //
float pwm=0;

// Sign of Roll and Previous Roll for Integral Wind-Up //
int sgnRoll, sgnPrevRoll;

/* Motor Pin Definition */
#define dir_pin 8
#define pwm_pin 6