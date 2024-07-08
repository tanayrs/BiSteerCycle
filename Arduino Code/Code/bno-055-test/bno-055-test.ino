/**
* Filter Testing for BNO-055 and MPU6050
* BNO-055 IMU Test Code from: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
* Modified to Plot Values on Serial Plotter as Compared to Printing on Serial Monitor.
* By: Jia Bhargava, Tanay Srinivasa
* Date Modified: 11 Jun 2024
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <elapsedMillis.h>
#include <KalmanFilter.h> // Repo: https://github.com/jarzebski/Arduino-KalmanFilter/tree/master //
#include <Adafruit_Sensor.h>
  
void setup(void) {
        startup_routine_bno();
        Serial.begin(9600);

}

void loop(void) {
        // calculate_bno_angle();
        // calculate_bno_angle_kalman();
        filter_testing();
        // mpu_kalman_test();
}
