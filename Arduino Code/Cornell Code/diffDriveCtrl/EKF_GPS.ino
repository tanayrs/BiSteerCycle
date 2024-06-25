/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * EKF_GPS.c
 *
 * Code generation for function 'EKF_GPS'
 *
 */

/* Include files */

/* Function Definitions */
void EKF_GPS(const double muPrev[3], const double sigPrev[9], const double
             odomData[2], const double measGPS[3], const double covQR[2], double
             muNew[3], double sigNew[9], bool isNewFix)
{
        static const signed char b[9] = { 1, 0, 0, 0, 1, 0, 0, 0, 1 };

        static const signed char iv[9] = { 1, 0, 0, 0, 1, 0, 0, 0, 1 };

        double B[9];
        double G[9];
        double Kgain[9];
        double T_B2I_tmp[9];
        double sigPred[9];
        double b_T_B2I_tmp[3];
        double muPred[3];
        double G_tmp_tmp;
        double L;
        double a21;
        double b_G_tmp_tmp;
        double c_G_tmp_tmp;
        double d_G_tmp_tmp;
        double maxval;
        double x_idx_0;
        int Kgain_tmp;
        int T_B2I_tmp_tmp;
        int r1;
        int r2;
        int r3;
        int rtemp;
        signed char i;
        signed char i1;
        signed char i2;

        /*  EKF runs one propagation of a generic extended kalman filter using odometry 
            information and sensor measurements 
            INPUTS
                muPrev          3x1 vector containing best guess of robots position 
                                before propagating the filter another step [x y theta] 
                sigPrev         3x3 covariance matrix describing the confidence in 
                                state estimate before propagating the filter another 
                                step 
                odomData        2x1 vector containing the odometry information from 
                                the most recent timestep [change in distance change in angle] 
                measGPS         3x1 vector of sensor measurements. (3x1, [x y theta]) 
          
            OUTPUTS 
                muNew           3x1 vector containing best guess of robots position 
                                after propagating the filter another step [x y theta] 
                sigNew          3x3 covariance matrix describing the confidence in 
                                state estimate propagating the filter another 
                                step 
          
            Cornell University - Fall 2020 
            Robert Whitney - rw429@cornell.edu 
         %%%%%%%%%%%%%%%%%%%% PREDICTION STEP %%%%%%%%%%%%%%%%%%%%% 
         process noise covariance matrix (constant size) 
         calculate control jacobian, pose prediction, and covariance prediction 
          GjacDiffDrive calculates the jacobian of a differential drive robot using 
          its current position and odometry information from the previous timestep 
          
            INPUTS 
                robotPose     3-by-1 pose vector in global coordinates (x,y,theta) 
                odomData        2x1 vector containing the odometry information from 
                                the most recent timestep 
            OUTPUTS 
                G               3x3 jacobian of the dynamics of the robot */

        if (odomData[1] == 0.0) {
                L = odomData[0];
        } else {
                maxval = odomData[0] / odomData[1];
                L = sqrt(2.0 * (1.0 - cos(odomData[1])) * (maxval * maxval));
        }

        G_tmp_tmp = cos(odomData[1]);
        b_G_tmp_tmp = sin(odomData[1]);
        G[0] = 1.0;
        G[3] = 0.0;
        c_G_tmp_tmp = cos(muPrev[2]);
        a21 = c_G_tmp_tmp * L;
        d_G_tmp_tmp = sin(muPrev[2]);
        maxval = d_G_tmp_tmp * L;
        G[6] = -(maxval * G_tmp_tmp + a21 * b_G_tmp_tmp);
        G[1] = 0.0;
        G[4] = 1.0;
        G[7] = a21 * G_tmp_tmp - maxval * b_G_tmp_tmp;

        /*  INTEGRATEODOM: calculates the new pose in the global frame given the 
          initial pose, and the distance and angle traveled since the function was 
          called.  Assumes constant linear and angular velocity 
          
            [newPose] = integrateOdom(oldPose,deltDist,deltTheta) 
          
            INPUTS 
                oldPose     3-by-1 pose vector in global coordinates (x,y,theta) 
                odomData    1x2 vector containing the odometry information from 
                                the most recent timestep 
          
            OUTPUTS 
                newPose     3-by-1 pose vector in global coordinates (x,y,theta) */

        G[2] = 0.0;
        G[5] = 0.0;
        G[8] = 1.0;

        /* calculate L, the shortest distance between the current pos and the pos 
         when integrateOdom was last called (a straight line). Must take care of 
         case when we have no curvature (infinite radius -> division by 0). */
        if (odomData[1] == 0.0) {
                maxval = odomData[0];
                if (odomData[0] < 0.0) {
                        maxval = -1.0;
                } else if (odomData[0] > 0.0) {
                        maxval = 1.0;
                } else {
                        if (odomData[0] == 0.0) {
                                maxval = 0.0;
                        }
                }
                L = maxval * odomData[0];
        } else {
                maxval = odomData[0] / odomData[1];
                L = sqrt(2.0 * (1.0 - cos(odomData[1])) * (maxval * maxval));
        }

        /* build transformation matrix from Body to Inertial 
         transform origin of current frame wrt previous frame to the inertial frame */
        maxval = odomData[0];
        if (odomData[0] < 0.0) {
                maxval = -1.0;
        } else if (odomData[0] > 0.0) {
                maxval = 1.0;
        } else {
                if (odomData[0] == 0.0) {
                        maxval = 0.0;
                }
        }

        a21 = odomData[0];
        if (odomData[0] < 0.0) {
                a21 = -1.0;
        } else if (odomData[0] > 0.0) {
                a21 = 1.0;
        } else {
                if (odomData[0] == 0.0) {
                        a21 = 0.0;
                }
        }

        /* new theta */
        T_B2I_tmp[0] = c_G_tmp_tmp;
        T_B2I_tmp[3] = -d_G_tmp_tmp;
        T_B2I_tmp[6] = muPrev[0];
        T_B2I_tmp[1] = d_G_tmp_tmp;
        T_B2I_tmp[4] = c_G_tmp_tmp;
        T_B2I_tmp[7] = muPrev[1];
        T_B2I_tmp[2] = 0.0;
        T_B2I_tmp[5] = 0.0;
        T_B2I_tmp[8] = 1.0;
        x_idx_0 = maxval * L * G_tmp_tmp;
        b_G_tmp_tmp *= a21 * L;
        for (r1 = 0; r1 < 3; r1++) {
                b_T_B2I_tmp[r1] = (T_B2I_tmp[r1] * x_idx_0 + T_B2I_tmp[r1 + 3] * b_G_tmp_tmp) + T_B2I_tmp[r1 + 6];
        }

        muPred[0] = b_T_B2I_tmp[0];
        muPred[1] = b_T_B2I_tmp[1];
        muPred[2] = muPrev[2] + odomData[1];
        for (r1 = 0; r1 < 3; r1++) {
                r2 = (int)G[r1];
                rtemp = (int)G[r1 + 3];
                maxval = G[r1 + 6];
                for (Kgain_tmp = 0; Kgain_tmp < 3; Kgain_tmp++) {
                        T_B2I_tmp[r1 + 3 * Kgain_tmp] = ((double)r2 * sigPrev[3 * Kgain_tmp] +
                        (double)rtemp * sigPrev[3 * Kgain_tmp + 1]) + maxval * sigPrev[3 *
                        Kgain_tmp + 2];
                }

                maxval = T_B2I_tmp[r1];
                a21 = T_B2I_tmp[r1 + 3];
                L = T_B2I_tmp[r1 + 6];
                for (r2 = 0; r2 < 3; r2++) {
                        rtemp = r1 + 3 * r2;
                        sigPred[rtemp] = ((maxval * G[r2] + a21 * G[r2 + 3]) + L * G[r2 + 6]) +
                        covQR[1] * (double)b[rtemp];
                }
        }

        /* %%%%%%%%%%%%%%%%%%%% UPDATE STEP %%%%%%%%%%%%%%%%%%%%% 
         if we have a new GPS measurement, update the prediction 
         measurement noise covariance matrix (not constant size) 
         Expected measurement will be the predicted pose 
         calculate Kalman gain */
        for (r1 = 0; r1 < 3; r1++) {
                i = b[r1];
                i1 = b[r1 + 3];
                i2 = b[r1 + 6];
                for (r2 = 0; r2 < 3; r2++) {
                        rtemp = 3 * r2 + 1;
                        Kgain_tmp = 3 * r2 + 2;
                        T_B2I_tmp_tmp = r1 + 3 * r2;
                        T_B2I_tmp[T_B2I_tmp_tmp] = ((double)i * sigPred[3 * r2] + (double)i1 *
                        sigPred[rtemp]) + (double)i2 * sigPred[Kgain_tmp];
                        G[T_B2I_tmp_tmp] = (sigPred[r1] * (double)iv[3 * r2] + sigPred[r1 + 3] *
                                                (double)iv[rtemp]) + sigPred[r1 + 6] * (double)
                        iv[Kgain_tmp];
                }

                maxval = T_B2I_tmp[r1];
                a21 = T_B2I_tmp[r1 + 3];
                L = T_B2I_tmp[r1 + 6];
                
                for (r2 = 0; r2 < 3; r2++) {
                        rtemp = r1 + 3 * r2;
                        B[rtemp] = ((maxval * (double)b[3 * r2] + a21 * (double)b[3 * r2 + 1]) + L
                                        * (double)b[3 * r2 + 2]) + covQR[0] * (double)b[rtemp];
                }
        }

        r1 = 0;
        r2 = 1;
        r3 = 2;
        maxval = fabs(B[0]);
        a21 = fabs(B[1]);
        if (a21 > maxval) {
                maxval = a21;
                r1 = 1;
                r2 = 0;
        }

        if (fabs(B[2]) > maxval) {
                r1 = 2;
                r2 = 1;
                r3 = 0;
        }

        B[r2] /= B[r1];
        B[r3] /= B[r1];
        B[r2 + 3] -= B[r2] * B[r1 + 3];
        B[r3 + 3] -= B[r3] * B[r1 + 3];
        B[r2 + 6] -= B[r2] * B[r1 + 6];
        B[r3 + 6] -= B[r3] * B[r1 + 6];
        if (fabs(B[r3 + 3]) > fabs(B[r2 + 3])) {
                rtemp = r2;
                r2 = r3;
                r3 = rtemp;
        }

        B[r3 + 3] /= B[r2 + 3];
        B[r3 + 6] -= B[r3 + 3] * B[r2 + 6];

        /* update state estimate and covariance estimate */
        Kgain[3 * r1] = G[0] / B[r1];
        maxval = B[r1 + 3];
        Kgain[3 * r2] = G[3] - Kgain[3 * r1] * maxval;
        a21 = B[r1 + 6];
        Kgain[3 * r3] = G[6] - Kgain[3 * r1] * a21;
        L = B[r2 + 3];
        Kgain[3 * r2] /= L;
        G_tmp_tmp = B[r2 + 6];
        Kgain[3 * r3] -= Kgain[3 * r2] * G_tmp_tmp;
        c_G_tmp_tmp = B[r3 + 6];
        Kgain[3 * r3] /= c_G_tmp_tmp;
        d_G_tmp_tmp = B[r3 + 3];
        Kgain[3 * r2] -= Kgain[3 * r3] * d_G_tmp_tmp;
        Kgain[3 * r1] -= Kgain[3 * r3] * B[r3];
        Kgain[3 * r1] -= Kgain[3 * r2] * B[r2];
        x_idx_0 = measGPS[0] - b_T_B2I_tmp[0];
        rtemp = 3 * r1 + 1;
        Kgain[rtemp] = G[1] / B[r1];
        Kgain_tmp = 3 * r2 + 1;
        Kgain[Kgain_tmp] = G[4] - Kgain[rtemp] * maxval;
        T_B2I_tmp_tmp = 3 * r3 + 1;
        Kgain[T_B2I_tmp_tmp] = G[7] - Kgain[rtemp] * a21;
        Kgain[Kgain_tmp] /= L;
        Kgain[T_B2I_tmp_tmp] -= Kgain[Kgain_tmp] * G_tmp_tmp;
        Kgain[T_B2I_tmp_tmp] /= c_G_tmp_tmp;
        Kgain[Kgain_tmp] -= Kgain[T_B2I_tmp_tmp] * d_G_tmp_tmp;
        Kgain[rtemp] -= Kgain[T_B2I_tmp_tmp] * B[r3];
        Kgain[rtemp] -= Kgain[Kgain_tmp] * B[r2];
        b_G_tmp_tmp = measGPS[1] - b_T_B2I_tmp[1];
        rtemp = 3 * r1 + 2;
        Kgain[rtemp] = G[2] / B[r1];
        Kgain_tmp = 3 * r2 + 2;
        Kgain[Kgain_tmp] = G[5] - Kgain[rtemp] * maxval;
        T_B2I_tmp_tmp = 3 * r3 + 2;
        Kgain[T_B2I_tmp_tmp] = G[8] - Kgain[rtemp] * a21;
        Kgain[Kgain_tmp] /= L;
        Kgain[T_B2I_tmp_tmp] -= Kgain[Kgain_tmp] * G_tmp_tmp;
        Kgain[T_B2I_tmp_tmp] /= c_G_tmp_tmp;
        Kgain[Kgain_tmp] -= Kgain[T_B2I_tmp_tmp] * d_G_tmp_tmp;
        Kgain[rtemp] -= Kgain[T_B2I_tmp_tmp] * B[r3];
        Kgain[rtemp] -= Kgain[Kgain_tmp] * B[r2];
        maxval = measGPS[2] - muPred[2];
        for (r1 = 0; r1 < 3; r1++) {
                muNew[r1] = muPred[r1] + ((Kgain[r1] * x_idx_0 + Kgain[r1 + 3] * b_G_tmp_tmp)
                + Kgain[r1 + 6] * maxval);
        }

        memset(&G[0], 0, 9U * sizeof(double));
        G[0] = 1.0;
        G[4] = 1.0;
        G[8] = 1.0;
        for (r1 = 0; r1 < 3; r1++) {
                maxval = Kgain[r1];
                a21 = Kgain[r1 + 3];
                L = Kgain[r1 + 6];
                for (r2 = 0; r2 < 3; r2++) {
                        T_B2I_tmp_tmp = r1 + 3 * r2;
                        T_B2I_tmp[T_B2I_tmp_tmp] = G[T_B2I_tmp_tmp] - ((maxval * (double)b[3 * r2]
                        + a21 * (double)b[3 * r2 + 1]) + L * (double)b[3 * r2 + 2]);
                }

                maxval = T_B2I_tmp[r1];
                a21 = T_B2I_tmp[r1 + 3];
                L = T_B2I_tmp[r1 + 6];
                for (r2 = 0; r2 < 3; r2++) {
                        sigNew[r1 + 3 * r2] = (maxval * sigPred[3 * r2] + a21 * sigPred[3 * r2 + 1])
                        + L * sigPred[3 * r2 + 2];
                }
        }

        /* ...otherwise, use prediction as the updated mu and sig */
}

/* End of code generation (EKF_GPS.c) */
