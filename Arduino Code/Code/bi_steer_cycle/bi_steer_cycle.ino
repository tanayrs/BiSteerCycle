/******************************************************************************************************************

Bi-Steer Cycle Code
By: Vishwas Gajera, Tanay Srinivasa, Jia Bhargava
Last Modified: 13 Jun 2024 11:40 AM

Functions Called in Setup and Loop are Defined in func.ino:
        - void startup_routine()                : Setting Encoder Pins to PULLUP and Initialises Ticks
        - void calculate_state()                : Updates Encoder Angle and IMU Angle
        - void updateEncoderData()              : Updating Encoder with Current Number of Ticks
        - void init_bno()                       : BNO-055 Initialisation and Calibration
        - void calculate_bno_angle()            : Calculate Angles from BNO-055 Sensor
        - void controller_segway()              : Controller of Wheel Inputs based on Lean Angle
        - void holdsteering(double degrees_F, double degrees_R): Sets Front and Rear Steering Angle based on Encoder Readings
        - void holdwheel(double degrees_F, double degrees_R)   : Sets Front and Rear Wheel Angle based on Encoder Readings
        - void writeToMotor()                   : Sets Steer and Drive Speeds to Front and Back Wheels
        - void logFeedback()                    : Print / Plot State Vars

**** Motor Configuration ****
rear Wheel Motor = Left Motor Driver M1 - Dir = 1, PWM = 0, PPR = , RPM = 450, EncA = 30, EncB = 29
rear Steer Motor = Left Motor Driver M2 - Dir = 3, PWM = 2, PPR = , RPM = 102, EncA = 32, EncB = 31
front Wheel Motor = Right Motor Driver M1 - Dir = 7, PWM = 6, PPR = , RPM = 450, EncA = 11, EncB = 10
front Steer Motor = Right Motor Driver M2 - Dir = 5, PWM = 4, PPR = , RPM = 103, EncA = 9 , EncB = 8

**** IMU Configuration ****
MPU 6050 - SCL = 19, SDA = 18
BNO-055  - NA
******************************************************************************************************************/


#define Battery_Voltage 12.0
#define loopTimeConstant 5000 // In micros // //5000
#define PWMResolution 4095


#include <Encoder.h> // Repo: https://github.com/PaulStoffregen/Encoder/blob/master //
#include <elapsedMillis.h>
#include <TrivikramEncoder.h>
#include <TrivikramController.h>
#include <CytronMotorDriver.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_BNO055.h>
#include <KalmanFilter.h> // Repo: https://github.com/jarzebski/Arduino-KalmanFilter/tree/master //
#include <Adafruit_Sensor.h>
#include <Wire.h>

/****************** Declaring GLobal Variables ******************/

#define steerMotorPPR 9048    //8540
#define wheelMotorPPR 1960.4    //2264
const double loopTimeConstSec = loopTimeConstant*1e-6f;
double sampling_time = loopTimeConstSec;

/* Bisteer Cycle Physical Model */
const float Ip = 2e-2; // MoI of body //
const float lF = 0.1;  // Distance of FW from COM //
const float lR = 0.1;  // Distance of RW from COM //
const float m  = 2.54; // Mass of power train //
const float r  = 0.03; // Radius of wheels in m //


/* IMU Definition */
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

/* Motor Driver */
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


/* Encoder and velocity */
double vel_cutoff_freq = 1000;

const int rearWheelEnc1 = 30; const int rearWheelEnc2 = 29;
const int rearSteerEnc1 = 32; const int rearSteerEnc2 = 31;
const int frontWheelEnc1 = 11; const int frontWheelEnc2 = 10;
const int frontSteerEnc1 = 9; const int frontSteerEnc2 = 8;
Encoder rearWheelEnc(rearWheelEnc1, rearWheelEnc2);
Encoder rearSteerEnc(rearSteerEnc2, rearSteerEnc1);     // Reversed to correct the orientation of the wheel angle //
Encoder frontWheelEnc(frontWheelEnc1, frontWheelEnc2);
Encoder frontSteerEnc(frontSteerEnc2, frontSteerEnc1);  // Reversed to correct the orientation of the wheel angle //

// Initilization of Objects of Class Encoder Data Processor //
EncoderDataProcessor rearWheelData(wheelMotorPPR, 0, true, false, vel_cutoff_freq, sampling_time); 
EncoderDataProcessor rearSteerData(steerMotorPPR, 0, false, false, vel_cutoff_freq, sampling_time);
EncoderDataProcessor frontWheelData(wheelMotorPPR, 0, true, true, vel_cutoff_freq, sampling_time);
EncoderDataProcessor frontSteerData(steerMotorPPR, 0, false, true, vel_cutoff_freq, sampling_time);

// global variables for derivative and integral controllers of wheel and steer motors
double prev_steer_error_F = 0;
double prev_steer_error_R = 0;
double integral_steer_F = 0;
double integral_steer_R = 0;

double prev_wheel_error_F = 0;
double prev_wheel_error_R = 0;
double integral_wheel_F = 0;
double integral_wheel_R = 0;

// Segway Controller gains 
#define Kp_lean 1700
#define Kd_lean  10
#define Kd_wheel 0
#define Ki_lean 0
double int_lean = 0;

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

/* State and control variables */
double phi, phi_dot;
double prv_sgn_phi = 0;

/* Trajectory Variables */
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

/* Timing and Code Control */
elapsedMicros loopTimeMicros;
elapsedMillis runTimeMillis;


/****************** Start of Code ******************/

void setup() {
        Serial.begin(9600);
        Serial.println("Starting Serial Print");

        //init_IMU();
        //delay(500);
        init_bno();
        delay(1000);

        loopTimeMicros = 0;
        runTimeMillis = 0;
        
        /* Setting Encoder Pins to PULLUP and Initialises Ticks */
        startup_routine();
}


void loop(){
        digitalWrite(13,HIGH);
        
        // Sets wheel motor to an angle with encoder readings
        // holdwheel(0, 90);

        // Updates Encoder Angle and IMU Angle 
        calculate_state();
        
        // Segway mode controller with IMU readings
        // controller_segway();
        
        // Sets Steer motor to an angle with encoder readings
        holdsteering(0,0);

        // Writes Inputs to Motors
        writeToMotor();   

        // Prints all relevant variables
        logFeedback();

        // Setting loop time to loopTimeConstant
        while(loopTimeMicros < loopTimeConstant)
                delayMicroseconds(50);
        loopTimeMicros = 0;

        digitalWrite(13,LOW);
}