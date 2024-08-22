/* Updates Encoder Angle and IMU Angle */

/**** Motor Configuration ****
rear Wheel Motor = Left Motor Driver M1 - Dir = 1, PWM = 0, PPR = , RPM = 450, EncA = 30, EncB = 29
rear Steer Motor = Left Motor Driver M2 - Dir = 3, PWM = 2, PPR = , RPM = 102, EncA = 32, EncB = 31
front Wheel Motor = Right Motor Driver M1 - Dir = 7, PWM = 6, PPR = , RPM = 450, EncA = 11, EncB = 10
front Steer Motor = Right Motor Driver M2 - Dir = 5, PWM = 4, PPR = , RPM = 103, EncA = 9 , EncB = 8

**** IMU Configuration ****
MPU 6050 - SCL = 19, SDA = 18
BNO-055  - NA
******************************************************************************************************************/

/* Updating IMU and Encoder Values */
void calculate_state() {
        updateEncoderData();
        calculate_bno_angle();
}

/* Updating Encoder with Current Number of Ticks */
void updateEncoderData() {
        // Reading Number of ticks from Encoder //
        long frontWheelTicks = frontWheelEnc.read();
        long frontSteerTicks = frontSteerEnc.read();
        long rearWheelTicks = rearWheelEnc.read();
        long rearSteerTicks = rearSteerEnc.read();

        // Updating Encoder Data Processor Objects //
        // Reference: void EncoderDataProcessor::update(long ticks,double steerAccumulatedTicks,double steerTicksOffset) //
        frontWheelData.update(frontWheelTicks, frontSteerTicks, 0);
        frontSteerData.update(frontSteerTicks, 0, 0);
        rearWheelData.update(rearWheelTicks, rearSteerTicks, 0);
        rearSteerData.update(rearSteerTicks, 0, 0);
}

/* BNO-055 Initialisation and Caliberation */
void init_bno() {
        if (!bno.begin()) {
                // Testing BNO-055 Connections //
                Serial.println("No BNO055 detected.\t\t Check your wiring or I2C ADDR");
                while (1);
        }
        bno.setExtCrystalUse(true);
}

/* Calculate Angles from BNO-055 Sensor */
void calculate_bno_angle() {
        sensors_event_t event;
        bno.getEvent( & event);
        previous_roll = roll;
        roll = event.orientation.z;
        phi = roll - phi_offset;
        bno.getEvent( & event, Adafruit_BNO055::VECTOR_GYROSCOPE);
        phi_dot = -event.gyro.x;
}