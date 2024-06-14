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
         calculate_bno_angle();
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
        phi = roll - 4;
        //phi = 0;
        bno.getEvent( & event, Adafruit_BNO055::VECTOR_GYROSCOPE);
        phi_dot = event.gyro.x;
}


/* Sets Steering Angle for Front and Rear Wheels */




/* Sets Steer and Drive Speeds to Front and Back Wheels */
void writeToMotor() {
        // Scaled Motor Speed Due to Different Speeds Observed In Forward and Reverse Directions //
        //frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput:(146.91/142.32)*frontWheelInput);
        frontSteerMotor.setSpeed(frontSteerInput);
        // rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput:(146.91/142.32)*rearWheelInput);
        rearSteerMotor.setSpeed(rearSteerInput);

        

        // Rear deadband: positive = 9, negative = -7 //
        if (rearWheelInput == 0) rearWheelMotor.setSpeed(0);
        else rearWheelMotor.setSpeed(rearWheelInput<0?rearWheelInput-7:rearWheelInput+9); 

        // Front deadband: positive = 11, negative = -11 //
        if (frontWheelInput == 0) frontWheelMotor.setSpeed(0);
        else frontWheelMotor.setSpeed(frontWheelInput<0?frontWheelInput-7:frontWheelInput+9); 
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