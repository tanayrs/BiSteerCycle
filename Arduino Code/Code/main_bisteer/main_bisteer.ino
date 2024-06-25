/******************************************************************************************************************

Bi-Steer Cycle Code
By: Vishwas Gajera, Tanay Srinivasa, Jia Bhargava
Last Modified: 14 Jun 2024 10:29 PM

Functions Called in Setup and Loop are Defined in func.ino:
        - void startup_routine()                : Setting Encoder Pins to PULLUP and Initialises Ticks
        - void calculate_state()                : Updates Encoder Angle and IMU Angle
        - void updateEncoderData()              : Updating Encoder with Current Number of Ticks/ Also used by deadband and motor calibration testing
        - float accelero_angle()                : Finds Pitch From Accelerometer -> Returns in Degrees
        - void init_IMU()                       : MPU 6050 Initialisation and Calibration
        - void init_bno()                       : BNO-055 Initialisation and Calibration
        - void calculate_mpu_angle_compfilter() : Calculate Angles from MPU6050 Sensor using a Complimentary Filter
        - void calculate_mpu_angle_kalman()     : Calculate Angles from MPU6050 Sensor using a Kalman Filter
        - void calculate_bno_angle()            : Calculate Angles from BNO-055 Sensor
        - void calculate_bno_angle_compfilter() : Calculate Angles from BNO-055 Sensor using a Complimentary Filter
        - void calculate_bno_angle_kalman()     : Calculate Angles from BNO-055 Sensor using a Kalman Filter
        - void controller_segway()              : Controller of Wheel Inputs based on Lean Angle
        - void controller_bicycle()             : Bicycle Controller (To be Implemented)
        - void holdsteering(double degrees_F, double degrees_R): Sets Front and Rear Steering Angle based on Encoder Readings
        - void holdwheel(double degrees_F, double degrees_R)   : Sets Front and Rear Wheel Angle based on Encoder Readings        
        - void writeToMotor()                   : Sets Steer and Drive Speeds to Front and Back Wheels
        - void motor_calibration()              : Calibrates the Wheel Motors for different Forward and Reverse Speeds for Sin Input
        - void motor_calibration_square()       : Calibrates the Wheel Motors for different Forward and Reverse Speeds for Square Input
        - void deadband_test()                  : Tests the Deadband of the Front and Rear Wheels using Triangle Input
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

#include "bisteer.h" 

/****************** Start of Code ******************/

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
        frontWheelInput = 0;
        rearWheelInput = 300;
        frontSteerInput = 500;
        rearSteerInput = 500;
        deadband_sign = 1;
        motor_calibration_sign = -1;
}

void loop(){
        digitalWrite(13,HIGH);
        
        // Sets Wheel to an Angle //
        // holdwheel(0*sin(millis()*1e-3), 0*sin(millis()*1e-3));
        // holdwheel(0, 90);

        // Updates Encoder Angle and IMU Angle //
        calculate_state();   
        
        // Calculates Drive Input //
        //  controller_segway();  // check direction of lean and motor direction cause changed wheel polarity and imu orient check PD direction
        //  controller_segway();  // check direction of lean and motor direction cause changed wheel polarity and imu orient check PD direction
        
        // Calculates Steer Input //
        holdsteering(90,90);     // takes front rear steer in degrees

        // Testing Deadband and Motor Calibration //
        // deadband_test();
        // motor_calibration_square();
        

         //controller_bicycle(0.48);
         //controller_rear_speed(0.48);
         //controller_front_speed(0.48);
        //frontWheelInput = -600;
        //rearWheelInput  = -600;
        // Writes Inputs to Motor //
        writeToMotor(); 
        // frontWheelMotor.setSpeed(210);  

        logFeedback();

        while(loopTimeMicros < loopTimeConstant)
                delayMicroseconds(10);

        //Serial.println(rearWheelData.speed()-frontWheelData.speed()); 
        //Serial.print(" "); 
        //Serial.println(frontWheelData.speed());
        //Serial.println(phi);
        //Serial.print(" ");
        //Serial.println(phi_dot);

        loopTimeMicros = 0;
        digitalWrite(13,LOW);
}