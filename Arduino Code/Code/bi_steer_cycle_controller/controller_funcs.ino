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
void controller_rear_speed(double velocity_rear){
        double Vr = velocity_rear;
        long double dt = loopTimeConstant * 1e-6;

        double speed_deg_target = (Vr*180)/(PI*r);     // target speed //

        double speed_error = (speed_deg_target - rearWheelData.speed());

        int_speed_error_rear += speed_error;

        double rear_wheel_inp = 0.5*(speed_error) - 0.0015*(speed_error - prev_speed_error_rear)/dt + 1*(int_speed_error_rear)*dt ;    //PD loop for controling speed. //Kp 0.07

        prev_speed_error_rear = speed_error;

        rearWheelInput = rear_wheel_inp;

        //Serial.println(speed_deg_target);

}

void controller_front_speed(double velocity_front){
        
        double Vf = velocity_front;

        long double dt = loopTimeConstant * 1e-6;

        double speed_deg_target = (Vf*180)/(PI*r);     // target speed //

        double speed_error = (speed_deg_target - frontWheelData.speed());

        int_speed_error_front += speed_error;

        double front_wheel_inp = 0.5*(speed_error) - 0.0015*(speed_error - prev_speed_error_front)/dt + 1*(int_speed_error_front)*dt ;    //PD loop for controling speed. //Kp 0.07

        prev_speed_error_front = speed_error;

        frontWheelInput = front_wheel_inp;

        //Serial.println(speed_deg_target);

}


void controller_bicycle(double rear_speed){     // designed for 0.48 m/s
      double Vr = rear_speed;

      
      
      double phi_rad = phi*(PI/180);
      double theta_F = frontSteerData.adjustedDegreesPosition()*(PI/180);
      double theta_R = rearSteerData.adjustedDegreesPosition()*(PI/180);

      double Vf = Vr*(sqrt( ((cos(phi_rad)*cos(phi_rad)) + (tan(theta_F)*tan(theta_F))) / ((cos(phi_rad)*cos(phi_rad)) + (tan(theta_R)*tan(theta_R))) ));

      double theta_F_target = 8*phi;
      controller_rear_speed(Vr);
      controller_front_speed(Vf);
      holdsteering(theta_F_target,0);




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
