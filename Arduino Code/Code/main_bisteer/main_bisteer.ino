/******************************************************************************************************************

Bi-Steer Cycle Code
By: Vishwas Gajera, Tanay Srinivasa, Jia Bhargava

Functions Called in Setup and Loop are Defined in IMU_encoder.ino, controller_funcs.ino, func.ino, log_feedback.ino. Functions in IMU_encoder.ino:
        - void calculate_state()                : Updates Encoder Angle and IMU Angle
        - void updateEncoderData()              : Updating Encoder with Current Number of Ticks/ Also used by deadband and motor calibration testing
        - void init_bno()                       : BNO-055 Initialisation and Calibration
        - void calculate_bno_angle()            : Calculate Angles from BNO-055 Sensor

Functions in controller_funcs.ino:
        - void controller_segway()              : PID Acceleration Controller for Front and Rear Wheel Motor in Segway Configuration
        - void controller_bicycle(double rear_speed)            : Calculation of Front and Rear Wheel Speed and Calling Rear and Front Speed Controller
        - void controller_rear_speed(double veloctiy_rear)      : Calculation of Rear Wheel Inputs using a Schmitt Trigger
        - void controller_front_speed(double veloctiy_front)    : Calculation of Front Wheel Inputs using a Schmitt Trigger
        - void controller_track_stand(double front_angle)       : PID Velocity Controller for Track Stand Mode
        - void holdwheel(double degrees_F, double degrees_R)    : PID Position Controller for Wheel Rotation of Front and Rear Wheels
        - void holdsteering(double degrees_F, double degrees_R) : PID Position Controller for Steering Angle of Front and Rear Wheels
        - void writeToMotor()                                   : Writes Calculated Input into the 4 Motors

Functions in func.ino:
        - void startup_routine()                                                        : Setting Encoder Pins to PULLUP and Initialises Ticks
        - float* PWPF(float controlSignal, float Uon, float Uoff, float prev_output)    : Calculates Schmitt Trigger Output
        - int sgn(double val)                                                           : Finds Sign of Value, returns -1 or 1

Functions in log_feedback.ino:
        - void logFeedback()                    : Print / Plot State Vars

**** Motor Configuration ****
rear Wheel Motor = Left Motor Driver M1 - Dir = 1, PWM = 0, PPR = , RPM = 450, EncA = 30, EncB = 29
rear Steer Motor = Left Motor Driver M2 - Dir = 3, PWM = 2, PPR = , RPM = 102, EncA = 32, EncB = 31
front Wheel Motor = Right Motor Driver M1 - Dir = 7, PWM = 6, PPR = , RPM = 450, EncA = 11, EncB = 10
front Steer Motor = Right Motor Driver M2 - Dir = 5, PWM = 4, PPR = , RPM = 103, EncA = 9 , EncB = 8

**** IMU Configuration ****
BNO-055 - SCL = 19, SDA = 18
******************************************************************************************************************/

#include "bisteer.h" 

/****************** Start of Code ******************/

void setup() {
        Serial.begin(115200);
        Serial.println("Starting Serial Print");

        // Setting Encoder Pins to PULLUP and Initialises Ticks //
        startup_routine();
}

void loop(){
        digitalWrite(13,HIGH);

        // Updates Encoder Angle and IMU Angle //
        calculate_state();

        // holdsteering(90,90);
        
        // Calculates Motor Inputs //
        // holdsteering(45,45);     // takes front rear steer in degrees
        // holdsteering(90,90);
        // holdwheel(90,90);
        
        // controller_track_stand(-45);
        controller_segway();
        // controller_bicycle(1);

        // controller_rear_speed(0.48);
        // controller_front_speed(0.48);

        // Writes Inputs to Motor //
        // frontWheelInput = 1000;
        // rearWheelInput = 1000;
        // frontSteerInput = 1000;
        // rearSteerInput = 1000;
        writeToMotor(); 

        // logFeedback();

        while(loopTimeMicros < loopTimeConstant)
                delayMicroseconds(10);

        loopTimeMicros = 0;
        digitalWrite(13,LOW);

        Serial.print(phi); Serial.print(" ");
        // Serial.print(frontWheelInput); Serial.print(" ");
        // Serial.print(rearWheelInput);
        Serial.println("");
}