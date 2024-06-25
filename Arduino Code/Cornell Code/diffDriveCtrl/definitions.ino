#include <Streaming.h>
#include <MPU6050.h>
#include <Wire.h>
#include <PID_v1.h>
#include <NMEAGPS.h>
#include <GPSport.h>
#include <math.h>
#include <string.h>

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
#define EN1 7   // PWM
#define EN2 2   // PWM
#define EN3 30  // PWM
#define EN4 29  // PWM

//Encoder interrupt pin mapping on teensy (4 encoders, 2 channels each, 8 total)
#define ENCD1_PINA 22 //GPIOC_PDIR, bits 1 & 2
#define ENCD1_PINB 23
#define ENCD2_PINA 11 //GPIOC_PDIR, bits 6 & 7
#define ENCD2_PINB 12
#define ENCD3_PINA 16 //GPIOB_PDIR, bits 0 & 1
#define ENCD3_PINB 17
#define ENCD4_PINA 19 //GPIOB_PDIR, bits 2 & 3
#define ENCD4_PINB 18

#define Pos_CntsPerRev    2160    //needs to be updated
#define Pos_Cnts2Rev      1/Pos_CntsPerRev
#define Vel_CntsPerRev    2160
#define Vel_Cnts2Rev      1/Vel_CntsPerRev
#define Pi                3.1415926
#define rad2deg           180/Pi
#define gyrLSB2Dps        1/65.5  //deg/(s*LSB) (for +/- 500 deg/s range)
#define accLSB2Gs         1/16384 //g/LSB       (for +/- 2g range, not really necessary if just calculating angles)
#define trackWidth        1       //distance between wheel centers


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

//EKF for localization
#define sigInit   10
#define prcssNse  10    //R
#define measNse   10    //Q

//Feedback Lin
#define epsilon 0.5   //smaller for tighter turns, larger for more lazy turns

//Motor pin mappings
const uint8_t MOTOR1[3] = {IN1, IN2, EN1}, MOTOR2[3] = {IN3, IN4, EN2},
const uint8_t MOTOR3[3] = {IN5, IN6, EN3}, MOTOR4[3] = {IN7, IN8, EN4};

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
double pos1_Ref = 0, pos1_Cmd = 0; //desired position [rad], command to motor 1 [LSB]
double vel2_Ref = 0, vel2_Cmd = 0; //desired velocity [rev/s], command to motor 2
double pos3_Ref = 0, pos3_Cmd = 0; //desired position [rad], command to motor 3
double vel4_Ref = 0, vel4_Cmd = 0; //desired velocity [rev/s], command to motor 4

//PID controllers for position and speed
PID ENCD1_PID(&ENCD1.Pos, &pos1_Cmd, &pos1_Ref, Kp_pos, Ki_pos, Kd_pos, DIRECT);  //position control
PID ENCD2_PID(&ENCD2.Vel, &vel2_Cmd, &vel2_Ref, Kp_vel, Ki_vel, Kd_vel, DIRECT);  //velocity control
PID ENCD3_PID(&ENCD3.Pos, &pos3_Cmd, &pos3_Ref, Kp_pos, Ki_pos, Kd_pos, DIRECT);  //position control
PID ENCD4_PID(&ENCD4.Vel, &vel4_Cmd, &vel4_Ref, Kp_vel, Ki_vel, Kd_vel, DIRECT);  //velocity control

//IMU
MPU6050 accelgyro;
int16_t ax, ay, az, gx, gy, gz;

//initialized to zero
float rollComp = 0, pitchComp = 0;
elapsedMicros lastTime_IMU;

// EKF initial mu and sigma
double myMu[3] = {0, 0, 0};   // X, Y, Theta
double mySigma[9] = {sigInit, 0, 0, 0, sigInit, 0, 0, 0, sigInit};

//GPS globals
static NMEAGPS  GPS;
static gps_fix  FIX;
bool isNewFix = false;

// goal positions [inertial frame]
double latRef, longRef;