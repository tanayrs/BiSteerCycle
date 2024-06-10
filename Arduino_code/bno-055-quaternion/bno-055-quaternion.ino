#include <Adafruit_BNO055.h>

Adafruit_BNO055 bno = Adafruit_BNO055();

void setup()
{
  Serial.begin(9600);
  Serial.println(F(""));
  Serial.println(F("BNO055: Compare three Euler techniques"));
  Serial.println(F(""));
  bno.begin();
}

void loop()
{
  // Using Adafruit library's axes conventions

//   if (1)
//   {
//     // BNO055 Euler - Broken! angles distort as pitch and roll increase
//     sensors_event_t event;
//     bno.getEvent(&event);
//     Serial.print(F("HeadingRollPitch from BNO055:  "));
//     Serial.print(event.orientation.x);  // heading, nose-right is positive
//     Serial.print(F(" "));
//     Serial.print(event.orientation.y);  // roll, rightwing-up is positive
//     Serial.print(F(" "));
//     Serial.print(event.orientation.z);  // pitch, nose-down is positive
//     Serial.println(F(""));
//   }

  if (1)
  {
    // Read quaternion, convert to Euler using Adafruit library
    imu::Quaternion q = bno.getQuat();
    q.normalize();
    imu::Vector<3> euler = q.toEuler();
    // imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
    euler.x() *= -180/M_PI;
    euler.y() *= -180/M_PI;
    euler.z() *= -180/M_PI;
    if (euler.x() < 0)
      euler.x() += 360;
//     Serial.print(F("HeadingRollPitch quat+library: "));
    Serial.print(euler.x());  // heading, nose-right is positive
    Serial.print(F(" "));
    Serial.print(euler.y());  // roll, rightwing-up is positive
    Serial.print(F(" "));
    Serial.print(euler.z());  // pitch, nose-down is positive
    Serial.println(F(""));
  }

    // // Read quaternion, convert to Euler using trigonometry
    // imu::Quaternion q = bno.getQuat();
    // float norm = 1 / sqrt(q.w() * q.w() + q.x() * q.x() + q.y() * q.y() + q.z() * q.z());
    // q.w() *= norm;
    // q.x() *= norm;
    // q.y() *= norm;
    // q.z() *= norm;
    // imu::Vector<3> euler;
    // euler.x() = -180/M_PI * atan2(q.w()*q.z() + q.x()*q.y(), 0.5 - q.y()*q.y() - q.z()*q.z());  // heading
    // euler.y() = -180/M_PI * asin(2 * (q.w()*q.y() - q.x()*q.z()));  // pitch
    // euler.z() = -180/M_PI * atan2(q.w()*q.x() + q.y()*q.z(), 0.5 - q.x()*q.x() - q.y()*q.y());  // roll
    // if (euler.x() < 0)
    //   euler.x() += 360;
    // // Serial.print(F("HeadingRollPitch quat+math:    "));
    // Serial.print(euler.x());  // heading, nose-right is positive
    // Serial.print(F(" "));
    // Serial.print(euler.y());  // roll, rightwing-up is positive
    // Serial.print(F(" "));
    // Serial.print(euler.z());  // pitch, nose-down is positive
    // Serial.println(F(""));


//   if (0)
//   {
//     // Read calibration status
//     uint8_t sys, gyro, accel, mag;
//     bno.getCalibration(&sys, &gyro, &accel, &mag);
//     Serial.print(F("Calibration: "));
//     Serial.print(sys, DEC);
//     Serial.print(F(" "));
//     Serial.print(gyro, DEC);
//     Serial.print(F(" "));
//     Serial.print(accel, DEC);
//     Serial.print(F(" "));
//     Serial.print(mag, DEC);
//     Serial.println(F(""));
//   }

//   Serial.println(F(""));
  delay(20);
}