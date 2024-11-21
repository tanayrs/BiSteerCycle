/******************************************************************************************************************

Segway Balancing Code
By: Vishwas Gajera, Tanay Srinivasa
Last Modified: 29 May 2024 10:28 AM

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

#include "constants.h"

void setup() {
        Serial.begin(9600);

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
        encoderValue = wheelEnc.read();
        
        lastt=t;
        t=micros();
        dt=(t-lastt)/1000000;

        segway_controller();
        writeToMotor();

        Serial.println(roll);
}