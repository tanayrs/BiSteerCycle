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

        // Serial.println(loopTimeMicros);
        if (loopTimeMicros > 5 * loopTimeConstant)
                Serial.println("ERROR - LOOP TIME EXCEEDED");
}