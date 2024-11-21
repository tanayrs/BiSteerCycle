/* Including Libraries */
#include <Encoder.h> // Repo: https://github.com/PaulStoffregen/Encoder/blob/master //
#include <elapsedMillis.h>
#include <TrivikramEncoder.h>
#include <CytronMotorDriver.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_BNO055.h>
#include <KalmanFilter.h> // Repo: https://github.com/jarzebski/Arduino-KalmanFilter/tree/master //
#include <Adafruit_Sensor.h>
#include "filter_lib.h"

/****************** Declaring GLobal Variables ******************/

#define Battery_Voltage 12.0
#define loopTimeConstant 10000 // In micros
#define PWMResolution 4095
#define steerMotorPPR 2262
#define wheelMotorPPR 490

const double loopTimeConstSec = loopTimeConstant*1e-6f;
double sampling_time = loopTimeConstSec;

/**** Bisteer Cycle Physical Model ****/
#define Ip 2e-2         // MoI of body //
#define lF 0.1          // Distance of FW from COM //
#define lR 0.1          // Distance of RW from COM //
#define m  2.54         // Mass of the vehicle //
#define r  0.03         // Radius of wheels in m //

/**** IMU Definition ****/
#define phi_offset 4.4 // Segway 4.9 / 4.6
// #define phi_offset 2.4 // Track-Stand 2.4

sensors_event_t a, g, temp;
float ax1, ay1, az1;
float gx1, gy1, gz1;
double previous_roll, elapsedTimeIMU, IMUFilterConstant,gyroAngleX, accelAngle,roll;
double IMUTimeConstant = 6.0;
elapsedMicros IMUTimeMicros;

// Pins are implicit in the wire library - SCL - 19, SDA 18 //
Adafruit_BNO055 bno = Adafruit_BNO055(55);

/**** Motor Driver ****/
const int rearWheelPWM = 0; const int rearWheelDir = 1;
const int rearSteerPWM = 3; const int rearSteerDir = 2;
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

const int frontWheelEnc1 = 30; const int frontWheelEnc2 = 29;
const int frontSteerEnc1 = 31; const int frontSteerEnc2 = 32;
const int rearWheelEnc1 = 11; const int rearWheelEnc2 = 10;
const int rearSteerEnc1 = 8; const int rearSteerEnc2 = 9;

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

// Hold Steer Error Variables //
double prev_steer_error_F = 0;
double prev_steer_error_R = 0;
double integral_steer_F = 0;
double integral_steer_R = 0;

// Hold Wheel Error Variables //
double prev_wheel_error_F = 0;
double prev_wheel_error_R = 0;
double integral_wheel_F = 0;
double integral_wheel_R = 0;

/**** Segway Controller ****/
#define Kp_lean 120 //600
#define Kd_lean 300 //400
#define Kd_wheel 0.3
#define Ki_lean 100
double int_lean = 0;
double Uf = 0;
double Ur = 0;

/**** Cycle Controller Varriables ****/
double prev_speed_error_rear = 0;
double prev_speed_error_front = 0;
double int_speed_error_front = 0;
double int_speed_error_rear  = 0;

float prev_PWPF_front = 0; 
float prev_PWPF_rear  = 0;

// PWPF Parameter //
const float Um = 1;    

// Initialize Previous Output State //
const float error_cutoff_freq = 20;
const float fw_kp = 10*PI/180; const float fw_kd = 0.1*PI/180;  
const float fs_kp = 1*PI/180; const float fs_kd = 0.1*PI/180;
const float rw_kp = 10*PI/180; const float rw_kd = 0.1*PI/180;  
const float rs_kp = 10*PI/180; const float rs_kd = 0.1*PI/180;

float rearWheelFF = 0;float rearSteerFF = 0;
float frontWheelFF = 0;float frontSteerFF = 0;

double vel_fw_kp = 0.1*PI/180; double vel_fw_ki = 10*PI/180; double vel_fw_kff = 12.0/1350.00;
double vel_fs_kp = 0.1*PI/180;  double vel_fs_ki = 10*PI/180; double vel_fs_kff = -12.0/650.00;
double vel_rw_kp = 0.1*PI/180; double vel_rw_ki = 10*PI/180; double vel_rw_kff = 12.0/1350.00;
double vel_rs_kp = 0.1*PI/180;  double vel_rs_ki = 10*PI/180; double vel_rs_kff = 12.0/650.00;

/**** State and Control Variables ****/
double phi, phi_dot;
int prv_sgn_phi = 0;

/**** Trajectory Variables ****/
double delF = 0;        // In degrees //
double delR = 0;        // In degrees //
double Vr   = 0;        // (1.0/r)*180.0/PI; // In dps, 1m/s in dps //
double Vf   = 0;        // Vr; // In dps //

double delF_dot = 0;    // In dps //
double delR_dot = 0;    // In dps //
double Vr_dot   = 0;    // In dps2 //
double Vf_dot   = 0;    // In dps2 //

double phiRefPos = 0;   // 0.1*180.0/PI;

/**** Timing and Code Control ****/
elapsedMicros loopTimeMicros;
elapsedMillis runTimeMillis;

/**** Track Stand Varliables ****/
#define Kp_track 140
#define Kd_track 40
#define Ki_track 10
#define Kd_track_wheel 1

double int_track, front_int_track, rear_int_track;
int prev_state = 1;
float gains_trackstand[4];

/**** Low Pass Filter ****/
lowpass_filter lpf_front_steer(2); 
lowpass_filter lpf_front_wheel(2); 
lowpass_filter lpf_rear_steer(2); 
lowpass_filter lpf_rear_wheel(2); 

/**** Motor Compensation ****/
#define frontWheelStaticDec -184
#define frontWheelStaticInc 221
#define frontWheelKineticDec 142
#define frontWheelKineticInc -133

#define rearWheelStaticDec -195
#define rearWheelStaticInc 186
#define rearWheelKineticDec 129
#define rearWheelKineticInc -133
