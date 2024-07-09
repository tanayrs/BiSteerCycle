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
                Serial.print(frontWheelInput); Serial.print(",");        
                Serial.print(frontWheelTicks); Serial.print(",");
                Serial.print(frontWheelData.speed()); Serial.print(",");
                // Serial.print(rearWheelInput); Serial.print(",");        
                Serial.print(rearWheelTicks); Serial.print(",");
                Serial.print(rearWheelData.speed());
                // Serial.print(frontSteerInput); Serial.print(",");        
                // Serial.print(frontSteerTicks); Serial.print(",");
                // Serial.print(frontSteerData.speed());
                // Serial.print(rearSteerInput); Serial.print(",");        
                // Serial.print(rearSteerTicks); Serial.print(",");
                // Serial.print(rearSteerData.speed());
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
        // Scaled Motor Speed Due to Different Speeds Observed In Forward and Reverse Directions: Not Used Anymore //
        // frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput:(146.91/142.32)*frontWheelInput);
        // rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput:(146.91/142.32)*rearWheelInput);
        
        // Directly Writing Input without any Compensation //
        // frontSteerMotor.setSpeed(frontSteerInput);
        // rearSteerMotor.setSpeed(rearSteerInput);
        frontWheelMotor.setSpeed(frontWheelInput);
        rearWheelMotor.setSpeed(rearWheelInput);
        
        // Deadband Compensation for all Motors //
        // Front Steer deadband: positive = 260, negative = -250 //
        if (frontSteerInput == 0) frontSteerMotor.setSpeed(0);
        else frontSteerMotor.setSpeed(frontSteerInput<0?frontSteerInput-250:frontSteerInput+260); 

        // Rear Steer deadband: positive = 130, negative = -190 //
        if (rearSteerInput == 0) rearSteerMotor.setSpeed(0);
        else rearSteerMotor.setSpeed(rearSteerInput<0?rearSteerInput-360:rearSteerInput+230); 

        // Rear deadband: positive = 170, negative = -160 //
        // if (rearWheelInput == 0) rearWheelMotor.setSpeed(0);
        // else rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput-105:rearWheelInput+115); 

        // Front deadband: positive = 215, negative = -170 //
        // if (frontWheelInput == 0) frontWheelMotor.setSpeed(0);
        // else frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput-125:frontWheelInput+155); 

        // Using Kinetic Coefficient for Motor Compensation //
        // if (frontWheelInput == 0){
        //         frontWheelMotor.setSpeed(0);
        // } else if (frontWheelData.speed() == 0){
        //         frontWheelMotor.setSpeed(frontWheelInput > 0? frontWheelInput+frontWheelStaticInc : frontWheelInput+frontWheelStaticDec);
        // } else {
        //         frontWheelMotor.setSpeed(frontWheelInput > 0? frontWheelInput+frontWheelKineticDec : frontWheelInput+frontWheelKineticInc);
        // }

        // if (rearWheelInput == 0){
        //         rearWheelMotor.setSpeed(0);
        // } else if (rearWheelData.speed() == 0) {
        //         rearWheelMotor.setSpeed(rearWheelInput > 0? rearWheelInput+rearWheelStaticInc : rearWheelInput+rearWheelStaticDec);
        // } else {
        //         rearWheelMotor.setSpeed(rearWheelInput > 0? rearWheelInput+rearWheelKineticDec : rearWheelInput+rearWheelKineticInc);
        // }
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

/* Finds the sign of num, returns -1 or 1 */
int sign(int num){
        return num<0?-1:1;
}
/* Testing Deadband for Wheel Motors using Triangle Input */
void deadband_test(){  
        if (millis() - prev_time > 100) {
                // Ramp Input //
                //   frontWheelInput = frontWheelInput>50?-50:frontWheelInput+1;
        
                // Triangle Input //
                if (zero_deadband_crosses < 21){
                        if ((frontWheelInput > 500)||(frontWheelInput < -500)) deadband_sign *= -1;
                        
                        frontWheelInput += (deadband_sign*20);
                        rearWheelInput = frontWheelInput;
                        
                        if (sign(frontWheelInput) != prev_input_sign){
                                zero_deadband_crosses++;
                                prev_input_sign = sign(frontWheelInput);
                        }
                } else {
                        frontWheelInput = 0;
                        rearWheelInput = 0;
                }

                // if ((rearWheelInput > 800)||(rearWheelInput < -800)) deadband_sign *= -1;
                // rearWheelInput += (deadband_sign*40);
                
                prev_time = millis();
        }  
}

/* Testing Deadband for Wheel Motors using Triangle Input */
void deadband_test_steer(){  
        if (millis() - prev_time > 200) {
                // Ramp Input //
                //   frontWheelInput = frontWheelInput>50?-50:frontWheelInput+1;
        
                // Triangle Input //
                // if ((frontSteerInput > 400)||(frontSteerInput < -400)) deadband_sign *= -1;
                // frontSteerInput += (deadband_sign*10);
                // prev_time = millis();

                if ((rearSteerInput > 400)||(rearSteerInput < -400)) deadband_sign *= -1;
                rearSteerInput += (deadband_sign*10);
                prev_time = millis();
        }  
}

/* Finding Maximum Input Value Corresponding to Max Motor Speed */
void max_input_speed(){
        if (millis() - prev_time > 100){
                frontSteerInput += 10;
                rearSteerInput += 10;
                prev_time = millis();
        }
        Serial.print(frontSteerInput); Serial.print(" "); Serial.print(frontSteerData.speed()); Serial.print(" ");
        Serial.print(rearSteerInput); Serial.print(" "); Serial.println(rearSteerData.speed());

        if (frontSteerInput > 2000) frontSteerInput = -2000;
        if (rearSteerInput > 2000) rearSteerInput = -2000;
}

/* PID Position Controller for Wheel Rotation of Front and Rear Wheels */
void holdwheel(double degrees_F, double degrees_R) {
        long double dt = loopTimeConstant * 1e-6;

        double EncTarget_F = degrees_F * (wheelMotorPPR) / 360; 
        double EncTarget_R = degrees_R * (wheelMotorPPR) / 360;

        double wheel_error_F = -(EncTarget_F - frontWheelEnc.read());
        double wheel_error_R = -(EncTarget_R - rearWheelEnc.read());
        
        frontWheelInput = 0.5 * (0.8 * (wheel_error_F) + 0.1 * ((wheel_error_F - prev_wheel_error_F)/dt) + 10*(integral_wheel_F)*dt);
        rearWheelInput = 0.5 * (0.8 * (wheel_error_R) + 0.1 * ((wheel_error_R - prev_wheel_error_R)/dt) + 10*(integral_wheel_R)*dt);

        prev_wheel_error_F = wheel_error_F;
        prev_wheel_error_R = wheel_error_R;

        // Integral Control is Activated at an Error within 5 degrees //
        if (wheel_error_F < 5 * wheelMotorPPR/360) integral_wheel_F += wheel_error_F; // 5 is for degrees can change //
        else integral_wheel_F = 0;
        if (wheel_error_R < 5 * wheelMotorPPR/360) integral_wheel_R += wheel_error_R;
        else integral_wheel_R = 0;

        // Setting the Maximum Input to The Wheels //
        // double acc = 100;
        // if (frontWheelInput > acc)
        //         frontWheelInput = acc;
        // if (frontWheelInput < -acc)
        //         frontWheelInput = -acc;
        // if (rearWheelInput > acc)
        //         rearWheelInput = acc;
        // if (rearWheelInput < -acc)
        //         rearWheelInput = -acc;
}

/* PID Position Controller for Steering Angle of Front and Rear Wheels */
void holdsteering(double degrees_F, double degrees_R) {
        long double dt = loopTimeConstant * 1e-6;

        double EncTarget_F = degrees_F * (steerMotorPPR) / 90;  // 90 Due to Quad Encoders //
        double EncTarget_R = degrees_R * (steerMotorPPR) / 90;

        double steer_error_F = EncTarget_F - frontSteerEnc.read();
        double steer_error_R = EncTarget_R - rearSteerEnc.read();

        frontSteerInput = 0.7 * (12 * steer_error_F + ((steer_error_F - prev_steer_error_F) / dt) + 20 * (integral_steer_F)*dt);
        rearSteerInput = 0.7 * (12 * steer_error_R + ((steer_error_R - prev_steer_error_R) / dt) + 20 * (integral_steer_R)*dt);

        integral_steer_F = integral_steer_F > 600? 600 : integral_steer_F;
        integral_steer_F = integral_steer_F < -600? -600 : integral_steer_F;
        integral_steer_R = integral_steer_R > 600? 600 : integral_steer_R;
        integral_steer_R = integral_steer_R < -600? -600 : integral_steer_R;

        if (steer_error_F < 5 * steerMotorPPR / 360) integral_steer_F += steer_error_F;  // 5 is for degrees can change //
        else integral_steer_F = 0;

        if (steer_error_R < 5 * steerMotorPPR / 360) integral_steer_R += steer_error_R;
        else integral_steer_R = 0;

        if (constrain(prev_steer_error_F,-1,1) != constrain(steer_error_F,-1,1)) integral_steer_F = 0;
        if (constrain(prev_steer_error_R,-1,1) != constrain(steer_error_R,-1,1)) integral_steer_R = 0;

        prev_steer_error_F = steer_error_F;
        prev_steer_error_R = steer_error_R;

        double acc = 1600;
        if (frontSteerInput > acc) frontSteerInput = acc;
        if (frontSteerInput < -acc) frontSteerInput = -acc;
        if (rearSteerInput > acc) rearSteerInput = acc;
        if (rearSteerInput < -acc) rearSteerInput = -acc;

        if (abs(steer_error_F) < 10) frontSteerInput = 0;
        if (abs(steer_error_R) < 10) rearSteerInput = 0;
}
  