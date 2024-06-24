/****************** Functions ******************/

/* Setting Encoder Pins to PULLUP and Initialises Ticks */
void startup_routine() {
        // Reference: void EncoderDataProcessor::update(long ticks,double steerAccumulatedTicks,double steerTicksOffset) //
        frontSteerData.update(0, 0, 0);
        rearSteerData.update(0, 0, 0);
        frontWheelData.update(0, 0, 0);
        rearWheelData.update(0, 0, 0);

        // Setting Encoder Pins to PULLUP //
        pinMode(rearWheelEnc1, INPUT_PULLUP);
        pinMode(rearWheelEnc2, INPUT_PULLUP);
        pinMode(rearSteerEnc1, INPUT_PULLUP);
        pinMode(rearSteerEnc2, INPUT_PULLUP);

        pinMode(frontWheelEnc1, INPUT_PULLUP);
        pinMode(frontWheelEnc2, INPUT_PULLUP);
        pinMode(frontSteerEnc1, INPUT_PULLUP);
        pinMode(frontSteerEnc2, INPUT_PULLUP);

        frontWheelInput = 0;
        rearWheelInput = 0;

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

        // For Measuring Deadband and Motor Calibration Step //
        if (millis() - prev_time_millis > 25){
                Serial.print(millis()); Serial.print(",");
                // Serial.print(rearWheelInput); Serial.print(",");        
                // Serial.print(rearWheelTicks); Serial.print(",");
                // Serial.print(rearWheelData.speed());
                Serial.print(frontWheelInput); Serial.print(",");        
                Serial.print(frontWheelTicks); Serial.print(",");
                Serial.print(frontWheelData.speed());
                Serial.println("");
                prev_time_millis = millis();
        }
}

/* MPU 6050 Initialisation and Calibration */
void init_IMU() {
        while (!mpu.begin()) {
                Serial.println("Failed to find MPU6050 chip");
                delay(500);
        }
        mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);
        mpu.setGyroRange(MPU6050_RANGE_250_DEG);
        mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
        Serial.println("MPU6050 Found!");

        int j = 0;
        while (j < 10) {
                mpu.getEvent( & a, & g, & temp); // Clearing rubbish values //
                delay(40);
                j++;
                ax1 = a.acceleration.x;
                ay1 = a.acceleration.y;
                az1 = a.acceleration.z;
        }

        mpu.getEvent( & a, & g, & temp);
        IMUTimeMicros = 0;
        ax1 = a.acceleration.x - accelXCorrection;
        ay1 = a.acceleration.y - accelYCorrection;
        az1 = a.acceleration.z - accelZCorrection;
        gx1 = g.gyro.x - gyroXCorrection;
        gy1 = g.gyro.y - gyroYCorrection;
        gz1 = g.gyro.z - gyroZCorrection;

        previous_roll = accelero_angle();
}

/* Sets Steer and Drive Speeds to Front and Back Wheels */
void writeToMotor() {
        // Scaled Motor Speed Due to Different Speeds Observed In Forward and Reverse Directions //
        // frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput:(146.91/142.32)*frontWheelInput);
        // frontSteerMotor.setSpeed(frontSteerInput);
        // rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput:(146.91/142.32)*rearWheelInput);
        // rearSteerMotor.setSpeed(rearSteerInput);

        frontWheelMotor.setSpeed(frontWheelInput);
        rearWheelMotor.setSpeed(rearWheelInput);

        // Rear deadband: positive = 170, negative = -160 //
        // if (rearWheelInput == 0) rearWheelMotor.setSpeed(0);
        // else rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput-105:rearWheelInput+115); 

        // Front deadband: positive = 215, negative = -170 //
        // if (frontWheelInput == 0) frontWheelMotor.setSpeed(0);
        // else frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput-125:frontWheelInput+155); 
}

/* Motor Calibration in Forward and Reverse Directions for Sin Input */
void motor_calibration(){  
        // Change to frontWheelInput for Front Wheel Testing //
        rearWheelInput =  100 * sin(millis()*1e-3);
        Serial.print(millis());
        Serial.print(" ");
        Serial.print(rearWheelData.speed());
        Serial.println("");
}

/* Motor Calibration in Forward and Reverse Directions for Square Input */
void motor_calibration_square(){
        if (millis() - prev_time > 5000){
                motor_calibration_sign *= -1;
                prev_time = millis();
        }
        
        // Change to frontWheelInput for Front Wheel Testing //
        rearWheelInput = (motor_calibration_sign > 0)? 150 : -150;
}

/* Testing Deadband using Triangle Input */
void deadband_test(){  
        if (millis() - prev_time > 100) {
                // Ramp Input //
                //   frontWheelInput = frontWheelInput>50?-50:frontWheelInput+1;
        
                // Triangle Input //
                if ((frontWheelInput > 800)||(frontWheelInput < -800)) deadband_sign *= -1;
                frontWheelInput += (deadband_sign*40);
                prev_time = millis();

                // if ((rearWheelInput > 800)||(rearWheelInput < -800)) deadband_sign *= -1;
                // rearWheelInput += (deadband_sign*40);
                // prev_time = millis();
        }  
}

/* Finding Maximum Input Value Corresponding to Max Motor Speed */
void max_input_speed(){
        if (millis() - prev_time > 100){
                frontWheelInput += 10;
                prev_time = millis();
        }
        Serial.print(frontWheelInput); Serial.print(" "); Serial.println(frontWheelData.speed());
}