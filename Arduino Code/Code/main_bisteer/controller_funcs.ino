/* PD Controller For Calculate Front Wheel Acceleration */
void controller_segway() {
        holdsteering(0,0);
        int sgn1 = sgn(phi);
        double dt = loopTimeConstant*1e-6;

        
        int_lean += Ki_lean*phi*dt;
        
        

        if (prv_sgn_phi != sgn1) {
                int_lean = 0;
                Uf = 0;
                Ur = 0;
        }

        int_lean = constrain(int_lean,-300,300);

        double front_acc, rear_acc;

        if (abs(phi) < 7.5) {
                front_acc = (Kp_lean * (phi) + Kd_lean * (phi_dot) + int_lean + 0*Kd_wheel * (frontWheelData.speed()));
                rear_acc =  (Kp_lean * (phi) + Kd_lean * (phi_dot) + int_lean + 0*Kd_wheel * (rearWheelData.speed()));
        } else {
                front_acc = 4*(Kp_lean * (phi) + 5000 * (phi_dot) + 2*int_lean + 0 * (frontWheelData.speed()));
                rear_acc =  4*(Kp_lean * (phi) + 5000 * (phi_dot) + 2*int_lean + 0 * (rearWheelData.speed())); 
        }

        prv_sgn_phi = sgn1;

        Uf += front_acc*dt;
        Ur += rear_acc*dt;
        
        if (abs(phi) > 20) {
                Uf = 0;
                Ur = 0;
                rear_acc = 0;
        }

        frontWheelInput = round(Uf);
        rearWheelInput  = round(Ur);
        // Serial.println(int_lean);
}
/******************************************************************************************************************************************************************************************************/
/* Calculation of Front and Rear Wheel Speed for Bicycle Mode */
void controller_bicycle(double rear_speed){     // designed for 0.48 m/s
        double Vr = rear_speed;

        double phi_rad = phi*(PI/180);
        double theta_F = frontSteerData.adjustedDegreesPosition()*(PI/180);
        double theta_R = rearSteerData.adjustedDegreesPosition()*(PI/180);

        double Vf = Vr*(sqrt( ((cos(phi_rad)*cos(phi_rad)) + (tan(theta_F)*tan(theta_F))) / ((cos(phi_rad)*cos(phi_rad)) + (tan(theta_R)*tan(theta_R))) ));

        double theta_F_target = 8*phi - 0.8*phi_dot;


        if (abs(theta_F_target) > 45){
                theta_F_target = sgn(theta_F_target)*45;
        }

        controller_rear_speed(Vr);
        controller_front_speed(Vf);
        if (abs(phi) > 20){
                frontWheelInput = 0;
                rearWheelInput = 0;
        }

        holdsteering(theta_F_target,0);
}   

/****************************************************************************************************************************************************************************************************/
/* Bicycle Controller for Rear Wheel Speed */
void controller_rear_speed(double velocity_rear){
        double Vr = velocity_rear;
        long double dt = loopTimeConstant * 1e-6;

        double speed_deg_target = (Vr*180)/(PI*r);     // target speed //

        double speed_error = (speed_deg_target - rearWheelData.speed());

        int_speed_error_rear += speed_error;
        int_speed_error_rear = constrain(int_speed_error_rear,-3000,3000);    // limiting integral error // integral windup

        float* PWPF_result = PWPF(speed_error,50,-7.5,prev_PWPF_rear);     // pwpf(error,uon,uoff,prev)
        float U = PWPF_result[0];
        prev_PWPF_rear = PWPF_result[1];


        double rear_wheel_inp = 0;

        if (U == 0) 
                rear_wheel_inp = 0.1*(speed_error) + 0*0.002*(speed_error - prev_speed_error_rear)/dt + 100*(int_speed_error_rear)*dt;
        else 
                rear_wheel_inp = 7*(speed_error) + 0*0.02*(speed_error - prev_speed_error_rear)/dt + 100*(int_speed_error_rear)*dt;

        //double rear_wheel_inp = 7*(speed_error) + 0.02*(speed_error - prev_speed_error_rear)/dt + 100*(int_speed_error_rear)*dt;


        // PD loop for controling speed. // Kp 0.07

        prev_speed_error_rear = speed_error;

        rear_wheel_inp = constrain(rear_wheel_inp,-4095,4095);

        rearWheelInput = rear_wheel_inp;

        // Serial.print(U);
        // Serial.print(" ");
        // Serial.println(prev_PWPF_rear);
        //Serial.println(rearWheelData.speed());
        //Serial.println(speed_error);
}

/****************************************************************************************************************************************************************************************************/
/* Bicycle Controller for Front Wheel Speed */
void controller_front_speed(double velocity_front){
        double Vf = velocity_front;

        long double dt = loopTimeConstant * 1e-6;

        double speed_deg_target = (Vf*180)/(PI*r);     // target speed //

        double speed_error = (speed_deg_target - frontWheelData.speed());

        int_speed_error_front += speed_error;
        int_speed_error_front = constrain(int_speed_error_front,-3000,3000);

        float* PWPF_result = PWPF(speed_error,50,-7.5,prev_PWPF_front);     // pwpf(error,uon,uoff,prev)
        float U = PWPF_result[0];
        prev_PWPF_front = PWPF_result[1];

        double front_wheel_inp = 0;
        if (U == 0) 
                front_wheel_inp = 0.1*(speed_error) + 0*0.002*(speed_error - prev_speed_error_front)/dt + 100*(int_speed_error_front)*dt ;    //PD loop for controling speed. //Kp 0.07
        else
                front_wheel_inp = 7*(speed_error) + 0*0.02*(speed_error - prev_speed_error_front)/dt + 100*(int_speed_error_front)*dt ;    //PD loop for controling speed. //Kp 0.07

        prev_speed_error_front = speed_error;

        prev_speed_error_front = speed_error;

        front_wheel_inp = constrain(front_wheel_inp,-4095,4095);

        frontWheelInput = front_wheel_inp;
}

/****************************************************************************************************************************************************************************************************/
/* PID Velocity Controller for Track Stand Mode */
void controller_track_stand(double front_angle){

        // If front wheel is turned left:
        //      If leaning left:
        //              Accelerate Forwards
        //      If leaning right:
        //              Accelerate Backwards
        // If front wheel is turned right:
        //      If leaning left:
        //              Accelerate Backwards
        //      If leaning right:
        //              Accelerate Forwards

        // now back calculate Vr to maintain rigid body constraint

        // lean towards left = +ve
        // lean towards right = -ve

        // steer towards left = +ve
        // steer towards right = -ve

        // Vf -> positive for if sign(psi) == sign(phi)
        // Vf -> negative for if sign(psi) != sign(phi)

        // Idea: Multiple control output with sign(psi)

        // Control Must be dependent on phi, phidot and phi_int

        // Finally integrate to get PID with respect to acceleation control

        long double dt = loopTimeConstant * 1e-6;

        // Fixing the front and rear steering at an angle and 0 for track stand
        holdsteering(-90, 0);
        // holdsteering(front_angle, 0);

        // based on phi (target = 0), PID loop will change rear velocity 
        double rear_acc = (Kp_track*(phi)) + (Kd_track * (phi_dot)) + (Ki_track * int_track) + (Kd_track_wheel * frontWheelData.speed());
        rear_acc *= sgn(front_angle);

        // Calculating front velocity based on rear velocity
        int_track += phi*dt;
        constrain(int_track,-300,300);

        double phi_rad = phi*(PI/180);
        double theta_F = frontSteerData.adjustedDegreesPosition()*(PI/180);
        double theta_R = rearSteerData.adjustedDegreesPosition()*(PI/180);
        double front_acc = rear_acc * (sqrt( ((cos(phi_rad)*cos(phi_rad)) + (tan(theta_F)*tan(theta_F))) / ((cos(phi_rad)*cos(phi_rad)) + (tan(theta_R)*tan(theta_R))) ));

        front_int_track = front_acc;
        rear_int_track = rear_acc;

        frontWheelInput = abs(phi)>20?0:front_int_track;
        rearWheelInput = abs(phi)>20?0:rear_int_track;

        Serial.print(phi); Serial.print(" ");
        Serial.print(Kp_track*(phi)); Serial.print(" ");
        Serial.print(Ki_track * int_track); Serial.print(" ");
        Serial.print(Kd_track * (phi_dot)); Serial.print(" ");
        Serial.print(rearWheelInput); Serial.print(" ");
        Serial.println(frontWheelInput);
}

/****************************************************************************************************************************************************************************************************/
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

/****************************************************************************************************************************************************************************************************/
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
        
        // Serial.print(EncTarget_F); Serial.print(" ");
        // Serial.print(steer_error_F); Serial.print(" ");
        // Serial.print(frontSteerEnc.read()); Serial.println("");
}

/****************************************************************************************************************************************************************************************************/

/* Writes Calculated Input into the 4 Motors */
void writeToMotor() {
        frontSteerInput = lpf_front_steer.filter(frontSteerInput);
        frontWheelInput = lpf_front_wheel.filter(frontWheelInput);
        rearSteerInput = lpf_rear_steer.filter(rearSteerInput);
        rearWheelInput = lpf_rear_wheel.filter(rearWheelInput);
        
        // Deadband Compensation for all Motors //
        // Front Steer deadband: positive = 260, negative = -250 //
        if (frontSteerInput == 0) frontSteerMotor.setSpeed(0);
        else frontSteerMotor.setSpeed(frontSteerInput<0?frontSteerInput-250:frontSteerInput+260); 

        // Rear Steer deadband: positive = 130, negative = -190 //
        if (rearSteerInput == 0) rearSteerMotor.setSpeed(0);
        else rearSteerMotor.setSpeed(rearSteerInput<0?rearSteerInput-360:rearSteerInput+230); 

        if (frontWheelInput == 0){
                frontWheelMotor.setSpeed(0);
        } else if (frontWheelData.speed() == 0){
                frontWheelMotor.setSpeed(frontWheelInput > 0? frontWheelInput+frontWheelStaticInc : frontWheelInput+frontWheelStaticDec);
        } else {
                frontWheelMotor.setSpeed(frontWheelInput > 0? frontWheelInput+frontWheelKineticDec : frontWheelInput+frontWheelKineticInc);
        }

        if (rearWheelInput == 0){
                rearWheelMotor.setSpeed(0);
        } else if (rearWheelData.speed() == 0) {
                rearWheelMotor.setSpeed(rearWheelInput > 0? rearWheelInput+rearWheelStaticInc : rearWheelInput+rearWheelStaticDec);
        } else {
                rearWheelMotor.setSpeed(rearWheelInput > 0? rearWheelInput+rearWheelKineticDec : rearWheelInput+rearWheelKineticInc);
        }
}

/****************************************************************************************************************************************************************************************************/
