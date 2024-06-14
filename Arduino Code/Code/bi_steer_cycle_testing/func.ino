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
        // if (millis() - prev_time_millis > 25){
        //         Serial.print(millis()); Serial.print(",");
        //         Serial.print(rearWheelInput); Serial.print(",");        
        //         Serial.print(rearWheelTicks); Serial.print(",");
        //         Serial.print(rearWheelData.speed());
        //         // Serial.print(frontWheelInput); Serial.print(",");        
        //         // Serial.print(frontWheelTicks); Serial.print(",");
        //         // Serial.print(frontWheelData.speed());
        //         Serial.println("");
        //         prev_time_millis = millis();
        // }
}

/* Finds Pitch From Accelerometer -> Returns in Degrees */
float accelero_angle() {
        return atan2(ay1, -az1) * 180.0 / PI;
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

/* PD Controller For Calculate Front Wheel Acceleration */
void controller_segway() {
        holdsteering(0,0);
        double sgn = constrain(phi,-1,1);
        double dt = loopTimeConstant*1e-6;
        int_lean += phi;

        if (prv_sgn_phi != sgn) {
                int_lean = 0;
                Uf = 0;
                Ur = 0;
        }

        double front_acc = (1*Kp_lean * (phi) + 1*Kd_lean * (phi_dot) + 0*Ki_lean*int_lean*dt + 0*Kd_wheel * (frontWheelData.speed())) * (PI / 180);
        double rear_acc = (1*Kp_lean * (phi) + 1*Kd_lean * (phi_dot) + 0*Ki_lean*int_lean*dt + 0*Kd_wheel * (rearWheelData.speed())) * (PI / 180);
 
        prv_sgn_phi = sgn;

        Uf += front_acc*dt;
        Ur += rear_acc*dt;
        
        if (abs(phi) > 20) {
                front_acc = 0;
                int_lean = 0;
                rear_acc = 0;
        }

        frontWheelInput = round(Uf);
        rearWheelInput  = round(Ur);
        // Serial.print(frontWheelInput);
        // Serial.print(" ");
        // Serial.println(rearWheelInput);
}

/* Bicycle Controller (To be Implemented) */
void controller_bicycle(double velocity_rear){
        double Vr = velocity_rear;
        double Vf = velocity_rear*1;

        long double dt = loopTimeConstant * 1e-6;

        double speed_deg_target = (Vr*180)/(PI*r);     // target speed //

        double speed_error = (speed_deg_target - rearWheelData.speed());

        double rear_wheel_inp = 0.1*(speed_error) + 0.01*(speed_error - prev_speed_error)/dt;    //PD loop for controling speed

        prev_speed_error = speed_error;

        rearWheelInput = rear_wheel_inp;

}

/* Sets Steering Angle for Front and Rear Wheels */
void holdsteering(double degrees_F, double degrees_R) {
        int sgnF = constrain(degrees_F, -1, 1);

        long double dt = loopTimeConstant * 1e-6;

        double EncTarget_F = (degrees_F + 0*sgnF) * (steerMotorPPR) / 360; // Add 3 in deadband //
        double EncTarget_R = degrees_R * (steerMotorPPR) / 360;

        double steer_error_F = EncTarget_F - frontSteerEnc.read();
        double steer_error_R = EncTarget_R - rearSteerEnc.read();
        

        frontSteerInput = 1 * (steer_error_F) + 0.05 * ((steer_error_F - prev_steer_error_F)/dt) + 5*(integral_steer_F)*dt;
        rearSteerInput =  1 * (steer_error_R) + 0.05 * ((steer_error_R - prev_steer_error_R)/dt) + 5*(integral_steer_R)*dt;


        prev_steer_error_F = steer_error_F;
        prev_steer_error_R = steer_error_R;

        if (steer_error_F < 5*steerMotorPPR/360) integral_steer_F += steer_error_F; // 5 is for degrees can change // 
        else integral_steer_F = 0;
         
        if(steer_error_R < 5*steerMotorPPR/360) integral_steer_R += steer_error_R;
        else integral_steer_R = 0;
        
        double acc = 100;
        
        if (frontSteerInput > acc)  frontSteerInput = acc;
        if (frontSteerInput < -acc) frontSteerInput = -acc;
        if (rearSteerInput > acc)   rearSteerInput = acc;
        if (rearSteerInput < -acc)  rearSteerInput = -acc;
}

/* Sets Wheel Angle for Front and Rear Wheels */
void holdwheel(double degrees_F, double degrees_R) {
        long double dt = loopTimeConstant * 1e-6;

        double EncTarget_F = degrees_F * (wheelMotorPPR) / 360; 
        double EncTarget_R = degrees_R * (wheelMotorPPR) / 360;

        double wheel_error_F = -(EncTarget_F - frontWheelEnc.read());
        double wheel_error_R = -(EncTarget_R - rearWheelEnc.read());

        // Serial.print(millis());
        // Serial.print(" ");
        // Serial.print(wheel_error_F * 360 / wheelMotorPPR);
        // Serial.print(" ");
        // Serial.print(wheel_error_R * 360 / wheelMotorPPR);
        // Serial.println("");
        
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

/* Sets Steer and Drive Speeds to Front and Back Wheels */
void writeToMotor() {
        // Scaled Motor Speed Due to Different Speeds Observed In Forward and Reverse Directions //
        // frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput:(146.91/142.32)*frontWheelInput);
        // frontSteerMotor.setSpeed(frontSteerInput);
        // rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput:(146.91/142.32)*rearWheelInput);
        // rearSteerMotor.setSpeed(rearSteerInput);

        // Rear deadband: positive = 9, negative = -7 //
        if (rearWheelInput == 0) rearWheelMotor.setSpeed(0);
        else rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput-7:rearWheelInput+9); 

        // Front deadband: positive = 11, negative = -11 //
        if (frontWheelInput == 0) frontWheelMotor.setSpeed(0);
        else frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput-7:frontWheelInput+9); 
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
        if (millis() - prev_time > 200) {
                // Ramp Input //
                //   frontWheelInput = frontWheelInput>50?-50:frontWheelInput+1;
        
                // Triangle Input //
                if ((frontWheelInput > 50)||(frontWheelInput < -50)) deadband_sign *= -1;
                frontWheelInput = frontWheelInput+deadband_sign;
                prev_time = millis();
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

/* Print / Plot State Vars */
void logFeedback() {
        // Serial.println("FWPos, RWPos, FSPos, RSPos");
        // Serial.print(frontWheelEnc.read());
        // Serial.print(" ");
        // Serial.print(frontSteerEnc.read());
        // Serial.print(" ");
        // Serial.print(rearWheelEnc.read());
        // Serial.print(" ");
        // Serial.print(rearSteerEnc.read());
        // Serial.print(" ");
        // Serial.print(frontWheelData.degreesPosition());
        // Serial.print(" ");
        // Serial.print(rearWheelData.degreesPosition());
        // Serial.print(" ");
        // Serial.print(frontSteerData.degreesPosition());
        // Serial.print(" ");
        // Serial.print(rearSteerData.degreesPosition());
        // Serial.print(" ");

        // Serial.println(rearWheelEnc.read());

        // Serial.println("ax     ay     az     gx     gy     gz  accAng     Ang");
        // Serial.print(ax1,3);
        // Serial.print(" ");
        // Serial.print(ay1,3);
        // Serial.print(" ");
        // Serial.print(az1,3);
        // Serial.print(" ");
        // Serial.print(gx1,3);
        // Serial.print(" ");
        // Serial.print(gy1,3);
        // Serial.print(" ");
        // Serial.print(gz1,3);
        // Serial.print(" ");
        // Serial.print(accelAngle,3);
        // Serial.print(" ");
        // Serial.print(roll,3);
        // Serial.print(" ");

        // Serial.print("\n");
        // Serial.print(frontWheelRefPos);
        // Serial.print(" ");
        // Serial.print(frontWheelController.error());
        // Serial.print(" ");
        // Serial.print(frontWheelData.ticks()*360.0/CPR);
        // Serial.print("     ");
        // Serial.print(frontWheelController.errorROC());
        // Serial.print("    ");
        // Serial.print(frontWheelController.controllerVoltage());
        // Serial.print(" ");
        // Serial.print(frontWheelController.outputVoltage());
        // Serial.print(" ");
        // Serial.print(frontWheelController.PWM());
        // Serial.print(" ");
        // Serial.println(frontWheelInput);
        // Serial.println("phi, phi_dot");
        // Serial.print(phi);
        // Serial.print(" ");
        // Serial.print(phi_dot);
        // Serial.print(" ");
        // Serial.print(frontWheelData.degreesPosition());
        // Serial.print(" ");
        // Serial.print(frontWheelData.speed());
        // Serial.print(" ");
        // Serial.print(frontWheelRefVel);
        // Serial.print(" ");
        // Serial.print(frontWheelController.omegaError());
        // Serial.print(" ");
        // Serial.print(frontWheelInput);

        Serial.println("phi phidot large phiErr");
        Serial.print(phi);
        Serial.print(" ");
        Serial.print(phi_dot);
        Serial.print(" ");
        Serial.print((phi_dot >= 5));
        Serial.print(" ");
        Serial.print(phiRefPos - phi);
        Serial.println("  ");
        Serial.print("\n");
        // Serial.print(ax1);
        // Serial.println(" ");
        // Serial.print(ay1);
        // Serial.println(" ");
        // Serial.print(az1);
        // Serial.println(" ");
        // Serial.println(gx1);
        Serial.println("Vrdot Vfdot delFdot delRdot     Vr  Vf  delR  delF");
        Serial.print(Vr_dot);
        Serial.print("   ");
        Serial.print(Vf_dot);
        Serial.print(" ");
        Serial.print(delF_dot);
        Serial.print(" ");
        Serial.print(delR_dot);
        Serial.print("     ");
        Serial.print(Vr);
        Serial.print(" ");
        Serial.print(Vf);
        Serial.print(" ");
        Serial.print(delR);
        Serial.print(" ");
        Serial.print(delF);
        Serial.print(" ");
        Serial.print("\n");
        Serial.print("\n");
        //Serial.print(" ");

        Serial.println("FWngle  FSang RWAng RSAng    FWSpeed FSSpeed RWSpeed RSSpeed");
        Serial.print(frontWheelData.adjustedDegreesPosition());
        Serial.print(" ");
        Serial.print(frontSteerData.adjustedDegreesPosition());
        Serial.print(" ");
        Serial.print(rearWheelData.adjustedDegreesPosition());
        Serial.print(" ");
        Serial.print(rearSteerData.adjustedDegreesPosition());
        Serial.print("     ");
        Serial.print(frontWheelData.speed());
        Serial.print(" ");
        Serial.print(frontSteerData.speed());
        Serial.print(" ");
        Serial.print(rearWheelData.speed());
        Serial.print(" ");
        Serial.print(rearSteerData.speed());
        Serial.print(" ");
        // Serial.print("\n");

        // Serial.println("FWREfVel FSRefPos RWRefVel RWRefPos");
        // Serial.print(frontWheelRefVel);
        // Serial.print(" ");
        // Serial.print(frontSteerRefPos);
        // Serial.print(" ");
        // Serial.print(rearWheelRefVel);
        // Serial.print(" ");
        // Serial.print(rearSteerRefPos);
        // Serial.print(" ");
        // Serial.print("\n");

        // Serial.println("FWIn  FSIn  RWIn  RSIn");
        // Serial.print(frontWheelInput);
        // Serial.print(" ");
        // Serial.print(frontSteerInput);
        // Serial.print(" ");
        // Serial.print(rearWheelInput);
        // Serial.print(" ");
        // Serial.print(rearSteerInput);
        // Serial.print(" ");

        //Serial.print("\n");
        //Serial.println(loopTimeMicros);
        //Serial.print("\n");

        Serial.println(loopTimeMicros);
        if (loopTimeMicros > 5 * loopTimeConstant)
                Serial.println("ERROR - LOOP TIME EXCEEDED");




}