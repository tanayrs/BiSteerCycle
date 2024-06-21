/* Updates Encoder Angle and IMU Angle */
void calculate_state() {
        updateEncoderData();
        // Choose Between MPU-Complimentary Filter, MPU-Kalman Filter,  BNO, BNO-Complimentary Filter, BNO-Kalman Filter //
        // calculate_mpu_angle_kalman();
        // calculate_mpu_angle_compfilter();
        // calculate_bno_angle();
        // calculate_bno_angle_compfilter();
        // calculate_bno_angle_kalman();
}

/* Finds Pitch From Accelerometer -> Returns in Degrees */
float accelero_angle() {
        return atan2(ay1, -az1) * 180.0 / PI;
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

/* Calculation of MPU6050 Angle using Complimentary Filter */
void calculate_mpu_angle_compfilter() {
        mpu.getEvent( & a, & g, & temp);
        elapsedTimeIMU = IMUTimeMicros / 1000.0;
        IMUTimeMicros = 0;
        IMUFilterConstant = IMUTimeConstant / (IMUTimeConstant + (elapsedTimeIMU / 1000.0));

        ax1 = a.acceleration.x - accelXCorrection;
        ay1 = a.acceleration.y - accelYCorrection;
        az1 = a.acceleration.z - accelZCorrection;
        gx1 = (g.gyro.x - gyroXCorrection) * 180.0 / PI; // Angle in degrees //

        accelAngle = accelero_angle();
        if (elapsedTimeIMU < 50)
                gyroAngleX = previous_roll + -gx1 * elapsedTimeIMU / 1000;
        else
                gyroAngleX = previous_roll;
        roll = ((IMUFilterConstant * gyroAngleX) + ((1 - IMUFilterConstant) * accelAngle));
        previous_roll = roll;
        phi = roll;
        phi_dot = -gx1;
}

/* Calculate Angles from MPU6050 Sensor using a Kalman Filter */
void calculate_mpu_angle_kalman() {
mpu.getEvent( & a, & g, & temp);
        elapsedTimeIMU = IMUTimeMicros / 1000.0;
        IMUTimeMicros = 0;
        IMUFilterConstant = IMUTimeConstant / (IMUTimeConstant + (elapsedTimeIMU / 1000.0));

        ax1 = a.acceleration.x - accelXCorrection;
        ay1 = a.acceleration.y - accelYCorrection;
        az1 = a.acceleration.z - accelZCorrection;
        gx1 = (g.gyro.x - gyroXCorrection) * 180.0 / PI; // Angle in degrees //

        accelAngle = accelero_angle();
        if (elapsedTimeIMU < 50)
                gyroAngleX = previous_roll + -gx1 * elapsedTimeIMU / 1000;
        else
                gyroAngleX = previous_roll;
        
        kalRoll = (kalmanX.update(accelero_angle(), gx1));
        phi = kalRoll;
        phi_dot = g.gyro.x;
}

/* Calculate Angles from BNO-055 Sensor */
void calculate_bno_angle() {
        sensors_event_t event;
        bno.getEvent( & event);
        previous_roll = roll;
        roll = event.orientation.y;
        phi = roll;
        bno.getEvent( & event, Adafruit_BNO055::VECTOR_GYROSCOPE);
        phi_dot = event.gyro.y;
}

/* Calculate Angles from BNO-055 Sensor using a Complimentary Filter */
void calculate_bno_angle_compfilter() {
        bno.getEvent( & a, Adafruit_BNO055::VECTOR_ACCELEROMETER);
        bno.getEvent( & g, Adafruit_BNO055::VECTOR_GYROSCOPE);

        elapsedTimeIMU = IMUTimeMicros / 1000.0;
        IMUTimeMicros = 0;
        IMUFilterConstant = IMUTimeConstant / (IMUTimeConstant + (elapsedTimeIMU / 1000.0));

        ax1 = a.acceleration.x - accelXCorrection;
        ay1 = a.acceleration.y - accelYCorrection;
        az1 = a.acceleration.z - accelZCorrection;
        gx1 = (g.gyro.x - gyroXCorrection) * 180.0 / PI; // Angle in degrees //

        accelAngle = accelero_angle();

        if (elapsedTimeIMU < 50)
                gyroAngleX = previous_roll + -gx1 * elapsedTimeIMU / 1000;
        else
                gyroAngleX = previous_roll;
        roll = ((IMUFilterConstant * gyroAngleX) + ((1 - IMUFilterConstant) * accelAngle));
        previous_roll = roll;
        phi = roll;
        phi_dot = -gx1;
}

/* Calculate Angles from BNO-055 Sensor using a Kalman Filter */
void calculate_bno_angle_kalman() {
        bno.getEvent( & a, Adafruit_BNO055::VECTOR_ACCELEROMETER);
        bno.getEvent( & g, Adafruit_BNO055::VECTOR_GYROSCOPE);
        float ax = a.acceleration.x;
        float ay = a.acceleration.y;
        float az = a.acceleration.z;
        float acc_angle_x = 180 * atan2(ay, sqrt(ax*ax + az*az))/PI; 
        kalRoll = (kalmanX.update(acc_angle_x, g.gyro.x));
        phi = -(kalRoll);        ///////////////////////////////////////////////////////////////////// correct this /////////////////////////////////////////////////////////////////
        phi_dot = -(g.gyro.x);
}