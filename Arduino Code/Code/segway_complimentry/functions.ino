void read_imu(){
        // === Read acceleromter data === //
        Wire.beginTransmission(MPU);
        Wire.write(0x3B); // Start with register 0x3B (ACCEL_XOUT_H)
        Wire.endTransmission(false);
        Wire.requestFrom(MPU, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
        //For a range of +-2g, we need to divide the raw values by 16384, according to the datasheet
        AccX = (Wire.read() << 8 | Wire.read()) / 16384.0; // X-axis value
        AccY = (Wire.read() << 8 | Wire.read()) / 16384.0; // Y-axis value
        AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0; // Z-axis value

        // Calculating Roll and Pitch from the accelerometer data
        accAngleX = (atan(AccY / sqrt(pow(AccX, 2) + pow(AccZ, 2))) * 180 / PI) + 1.68; // AccErrorX ~(1.98) See the calculate_IMU_error()custom function for more details
        accAngleY = (atan(-1 * AccX / sqrt(pow(AccY, 2) + pow(AccZ, 2))) * 180 / PI) + 1.35; // AccErrorY ~(-0.21)

        // === Read gyroscope data === //
        previousTime = currentTime;        // Previous time is stored before the actual time read
        currentTime = millis();            // Current time actual time read
        elapsedTime = (currentTime - previousTime) / 1000; // Divide by 1000 to get seconds
        Wire.beginTransmission(MPU);
        Wire.write(0x43); // Gyro data first register address 0x43
        Wire.endTransmission(false);
        Wire.requestFrom(MPU, 6, true); // Read 4 registers total, each axis value is stored in 2 registers
        GyroX = (Wire.read() << 8 | Wire.read()) / 131.0; // For a 250deg/s range we have to divide first the raw value by 131.0, according to the datasheet
        GyroY = (Wire.read() << 8 | Wire.read()) / 131.0;
        GyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;

        // Correct the outputs with the calculated error values
        GyroX = GyroX + 3.52; // GyroErrorX ~(-1.72)
        GyroY = GyroY + 1.46; // GyroErrorY ~(-0.73)
        GyroZ = GyroZ + 0.08; // GyroErrorZ ~ (-0.03)

        // Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
        gyroAngleX = gyroAngleX + GyroX * elapsedTime; // deg/s * s = deg
        gyroAngleY = gyroAngleY + GyroY * elapsedTime;
        yaw =  yaw + GyroZ * elapsedTime;

        // Complementary filter - combine acceleromter and gyro angle values
        roll = (0.98 * gyroAngleX) + (0.02 * accAngleX);
        pitch =(0.98 * gyroAngleY) + (0.02 * accAngleY);

        gyroAngleX=roll;     //corrects the gyroAngleX and y else senser reading gyroAnglex and y starts to drift
        gyroAngleY=pitch;

        // Print the values on the serial monitor
        // Serial.print(roll); Serial.print(" ");
        //Serial.print("/");
        // Serial.print(pitch);
        //Serial.print("/");
        //Serial.println(yaw);
}

void calculate_IMU_error() {
        // We can call this funtion in the setup section to calculate the accelerometer and gyro data error. From here we will get the error values used in the above equations printed on the Serial Monitor.
        // Note that we should place the IMU flat in order to get the proper values, so that we then can the correct values
        // Read accelerometer values 200 times
        while (c < 200) {
                Wire.beginTransmission(MPU);
                Wire.write(0x3B);
                Wire.endTransmission(false);
                Wire.requestFrom(MPU, 6, true);
                AccX = (Wire.read() << 8 | Wire.read()) / 16384.0 ;
                AccY = (Wire.read() << 8 | Wire.read()) / 16384.0 ;
                AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0 ;
                // Sum all readings
                AccErrorX = AccErrorX + ((atan((AccY) / sqrt(pow((AccX), 2) + pow((AccZ), 2))) * 180 / PI));
                AccErrorY = AccErrorY + ((atan(-1 * (AccX) / sqrt(pow((AccY), 2) + pow((AccZ), 2))) * 180 / PI));
                c++;
        }
        //Divide the sum by 200 to get the error value
        AccErrorX = AccErrorX / 200;
        AccErrorY = AccErrorY / 200;
        c = 0;
        // Read gyro values 200 times
        while (c < 200) {
                Wire.beginTransmission(MPU);
                Wire.write(0x43);
                Wire.endTransmission(false);
                Wire.requestFrom(MPU, 6, true);
                GyroX = Wire.read() << 8 | Wire.read();
                GyroY = Wire.read() << 8 | Wire.read();
                GyroZ = Wire.read() << 8 | Wire.read();
                // Sum all readings
                GyroErrorX = GyroErrorX + (GyroX / 131.0);
                GyroErrorY = GyroErrorY + (GyroY / 131.0);
                GyroErrorZ = GyroErrorZ + (GyroZ / 131.0);
                c++;
        }
        //Divide the sum by 200 to get the error value
        GyroErrorX = GyroErrorX / 200;
        GyroErrorY = GyroErrorY / 200;
        GyroErrorZ = GyroErrorZ / 200;
        // Print the error values on the Serial Monitor
        Serial.print("AccErrorX: ");
        Serial.println(AccErrorX);
        Serial.print("AccErrorY: ");
        Serial.println(AccErrorY);
        Serial.print("GyroErrorX: ");
        Serial.println(GyroErrorX);
        Serial.print("GyroErrorY: ");
        Serial.println(GyroErrorY);
        Serial.print("GyroErrorZ: ");
        Serial.println(GyroErrorZ);
}

void segway_controller() {
        sgnRoll = (roll > 0)? 1 : -1;

        error_roll = target_roll-roll;
        error_enc = (target_enc - (encoderValue/8530.0))*2*pi;   //8530 encoder constant 8530 interupts per round //

        if (fabs(error_roll) < deadzone ){
                u=0;
                pwm=fabs(u);
        } else {
                // Error Function Calculation //
                int_lean += (error_roll)*dt;
                int_lean = constrain(int_lean,-20,20);

                last_error_roll=error_roll;
                last_error_enc=error_enc;

                u=(Kp*error_roll)+(-Kd*GyroX)+(Ki*int_lean)+(Kd_wheel*(error_enc-last_error_enc)/dt);
                
                pwm=fabs(u);
                if (pwm > 255) pwm=255;
        }

        // If Lean > 20 Degrees, stop moving //
        if (fabs(roll)>20) pwm=0;

        // Integral Wind-Up //
        if (sgnRoll != sgnPrevRoll)
                int_lean = 0;
        sgnPrevRoll = sgnRoll;
}

void writeToMotor(){
        if (micros() - LoopTimer > 3000){
                wheelMotor.setSpeed(sgnRoll*pwm);
                LoopTimer=micros();
        }
}