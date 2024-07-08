#include <MPU6050_tockn.h>

MPU6050 mpu6050(Wire,0.02,0.998);
 
KalmanFilter kalmanX(0.0005, 0.005, 0.1);  //(Q_angle, Q_bais, R)
KalmanFilter kalmanY(0.0005, 0.005, 0.1);

float accPitch = 0;
float accRoll = 0;

float kalPitch = 0;
float kalRoll = 0;

float roll = 0.0;

void startup_routine_mpu(){
        Serial.begin(115200);
        Serial.println("Begin Serial Print");
        Wire.begin();
        mpu6050.begin();
        mpu6050.setGywroOffsets(-3.68,-1.50,-0.08);
}

void mpu_kalman_test(){
        mpu6050.update();
        kalRoll = (kalmanX.update(mpu6050.getAccAngleX(), mpu6050.getGyroX()));
        kalRoll = constrain(kalRoll,-60,60);
        Serial.println(kalRoll,1);
        delay(50);
}