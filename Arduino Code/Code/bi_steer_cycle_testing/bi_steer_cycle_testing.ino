/******************************************************************************************************************

Bi-Steer Cycle Code
By: Vishwas Gajera, Tanay Srinivasa, Jia Bhargava
Last Modified: 1 Jul 2024

Functions Called in Setup and Loop are Defined in func.ino, imu.ino, and log_feedback.ino. Functions in func.ino:
        - void startup_routine()                : Setting Encoder Pins to PULLUP and Initialises Ticks
        - void updateEncoderData()              : Updating Encoder with Current Number of Ticks/ Also used by deadband and motor calibration testing
        - void init_IMU()                       : MPU 6050 Initialisation and Calibration
        - void writeToMotor()                   : Sets Steer and Drive Speeds to Front and Back Wheels
        - void motor_calibration()              : Calibrates the Wheel Motors for different Forward and Reverse Speeds for Sin Input
        - void motor_calibration_square()       : Calibrates the Wheel Motors for different Forward and Reverse Speeds for Square Input
        - int sign(double num)                  : Finds the sign of num, returns -1 or 1
        - void deadband_test()                  : Tests the Deadband of the Front and Rear Wheel Motors using Triangle Input
        - void deadband_test_steer()            : Tests the Deadband of the Front and Rear Steer Motors using Triangle Input
        - void max_input_speed()                : Finding Maximum Input Value Corresponding to Max Motor Speed

Functions in imu.ino:
        - void calculate_state()                : Updates Encoder Angle and IMU Angle
        - float accelero_angle()                : Finds Pitch From Accelerometer -> Returns in Degrees
        - void init_bno()                       : BNO-055 Initialisation and Calibration
        - void calculate_mpu_angle_compfilter() : Calculate Angles from MPU6050 Sensor using a Complimentary Filter
        - void calculate_mpu_angle_kalman()     : Calculate Angles from MPU6050 Sensor using a Kalman Filter
        - void calculate_bno_angle()            : Calculate Angles from BNO-055 Sensor
        - void calculate_bno_angle_compfilter() : Calculate Angles from BNO-055 Sensor using a Complimentary Filter
        - void calculate_bno_angle_kalman()     : Calculate Angles from BNO-055 Sensor using a Kalman Filter
        
Functions in log_feedback.ino:
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

/****************** Start of Code ******************/
#include "constants.h"

void setup() {
        Serial.begin(115200);
        Serial.println("Starting Serial Print");
        
        //init_IMU();
        //delay(500);
        init_bno();
        delay(1000);

        loopTimeMicros = 0;
        runTimeMillis = 0;
        
        // Setting Encoder Pins to PULLUP and Initialises Ticks //
        startup_routine();
        analogWriteResolution(12);

        // For the Deadband Testing and Motor Calibration //
        prev_time = millis();
        prev_time_millis = millis();
        zero_deadband_crosses = 0;
        prev_input_sign = 1;
        
        frontWheelInput = 0;
        rearWheelInput = 0;
        frontSteerInput = 0;
        rearSteerInput = 0;
        
        deadband_sign = 1;
        motor_calibration_sign = -1;
}

void loop(){
        digitalWrite(13,HIGH);

        // Updates Encoder Angle and IMU Angle //
        calculate_state();
        
        // Testing Deadband and Motor Calibration //
        holdsteering(0,0);
        deadband_test();
        // deadband_test_steer();
        // motor_calibration_square();
        // max_input_speed();

        // Writes Inputs to Motor //
        // lowpassfilter();
        writeToMotor();   

        while(loopTimeMicros < loopTimeConstant)
                delayMicroseconds(50);

        // logFeedback();

        loopTimeMicros = 0;
        digitalWrite(13,LOW);
}