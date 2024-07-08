/* Incluiding Libraries */
#include <Encoder.h> // Repo: https://github.com/PaulStoffregen/Encoder/blob/master //
#include <elapsedMillis.h>
#include <TrivikramEncoder.h>
#include <CytronMotorDriver.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_BNO055.h>
#include <KalmanFilter.h> // Repo: https://github.com/jarzebski/Arduino-KalmanFilter/tree/master //
#include <Adafruit_Sensor.h>
#include <Wire.h>

/****************** Declaring GLobal Variables ******************/

#define Battery_Voltage 12.0
#define loopTimeConstant 10000 // In micros // //5000
#define PWMResolution 4095
#define steerMotorPPR 2262    //8540
#define wheelMotorPPR 490    //2264

const double loopTimeConstSec = loopTimeConstant*1e-6f;
double sampling_time = loopTimeConstSec;

/**** Bisteer Cycle Physical Model ****/
#define Ip 2e-2         // MoI of body //
#define lF 0.1          // Distance of FW from COM //
#define lR 0.1          // Distance of RW from COM //
#define m  2.54         // Mass of the vehicle //
#define r  0.03         // Radius of wheels in m //

/**** IMU Definition ****/
#define gyroXCorrection -0.0465
#define gyroYCorrection  0.0201
#define gyroZCorrection  0.0035

#define accelXCorrection  0.0739
#define accelYCorrection -0.1106
#define accelZCorrection -1.6547

sensors_event_t a, g, temp;
float ax1, ay1, az1;
float gx1, gy1, gz1;
double previous_roll, elapsedTimeIMU, IMUFilterConstant,gyroAngleX, accelAngle,roll;
double IMUTimeConstant = 6.0;
elapsedMicros IMUTimeMicros;

// MPU-6050 If Used //
// Pins are implicit in the wire library - SCL - 19, SDA 18 //
Adafruit_MPU6050 mpu;

// BNO-055 If Used //
Adafruit_BNO055 bno = Adafruit_BNO055(55);

// Kalman Filter if Used //
KalmanFilter kalmanX(0.005, 0.00, 0.1);  //(Q_angle, Q_bais, R) //
float kalRoll = 0;

/**** Motor Driver ****/
const int rearWheelPWM = 0; const int rearWheelDir = 1;
const int rearSteerPWM = 2; const int rearSteerDir = 3;
const int frontWheelPWM = 6;  const int frontWheelDir = 7;
const int frontSteerPWM = 5;  const int frontSteerDir = 4;

CytronMD rearWheelMotor(PWM_DIR, rearWheelPWM, rearWheelDir);
CytronMD rearSteerMotor(PWM_DIR, rearSteerPWM, rearSteerDir);
CytronMD frontWheelMotor(PWM_DIR, frontWheelPWM, frontWheelDir);
CytronMD frontSteerMotor(PWM_DIR, frontSteerPWM, frontSteerDir);

int rearWheelInput; int frontWheelInput;
int rearSteerInput; int frontSteerInput;

/**** Encoder and velocity ****/
double vel_cutoff_freq = 1000;

const int rearWheelEnc1 = 30; const int rearWheelEnc2 = 29;
const int rearSteerEnc1 = 32; const int rearSteerEnc2 = 31;
const int frontWheelEnc1 = 11; const int frontWheelEnc2 = 10;
const int frontSteerEnc1 = 9; const int frontSteerEnc2 = 8;

// Encoder Objects to Read Encoder Ticks //
Encoder rearWheelEnc(rearWheelEnc1, rearWheelEnc2);
Encoder rearSteerEnc(rearSteerEnc2, rearSteerEnc1);
Encoder frontWheelEnc(frontWheelEnc1, frontWheelEnc2);
Encoder frontSteerEnc(frontSteerEnc2, frontSteerEnc1);

// Encoder Objects to Store Encoder Ticks and Speed //
EncoderDataProcessor rearWheelData(wheelMotorPPR, 0, true, false, vel_cutoff_freq, sampling_time); 
EncoderDataProcessor rearSteerData(steerMotorPPR, 0, false, false, vel_cutoff_freq, sampling_time);
EncoderDataProcessor frontWheelData(wheelMotorPPR, 0, true, true, vel_cutoff_freq, sampling_time);
EncoderDataProcessor frontSteerData(steerMotorPPR, 0, false, true, vel_cutoff_freq, sampling_time);

/**** State and control variables ****/
double phi, phi_dot;
double prv_sgn_phi = 0;

/**** Trajectory Variables ****/
double delF = 0;        // In degrees //
double delR = 0;        // In degrees //
double Vr   = 0;        // (1.0/r)*180.0/PI; // In dps, 1m/s in dps //
double Vf   = 0;        // Vr; // In dps //

double delF_dot = 0;    // In dps //
double delR_dot = 0;    // In dps //
double Vr_dot   = 0;    // In dps2 //
double Vf_dot   = 0;    // In dps2 //

double rearWheelRefPos;double rearWheelRefVel;
double rearSteerRefPos;double rearSteerRefVel;
double frontWheelRefPos;double frontWheelRefVel;
double frontSteerRefPos;double frontSteerRefVel;

// Give the reference of phi here. For constant delF, delR,Vr or Vf, we can change the gains of the balance controller //
double phiRefPos = 0;   // 0.1*180.0/PI;
double phiRefVel;

/**** Timing and Code Control ****/
elapsedMicros loopTimeMicros;
elapsedMillis runTimeMillis;

// For Deadband and Motor Calibration Square //
int prev_time, prev_time_millis;
int deadband_sign, motor_calibration_sign;
int zero_deadband_crosses, prev_input_sign;

/**** Motor Compensation ****/
#define frontWheelStaticDec -170
#define frontWheelStaticInc 200
#define frontWheelKineticDec 130
#define frontWheelKineticInc -120

#define rearWheelStaticDec -175
#define rearWheelStaticInc 180
#define rearWheelKineticDec 125
#define rearWheelKineticInc -155