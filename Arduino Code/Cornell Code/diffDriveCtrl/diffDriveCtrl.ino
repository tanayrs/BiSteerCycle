
/*
        Encoder Method : http://makeatronics.blogspot.com/2013/02/efficiently-reading-quadrature-with.html
        Teensy Datasheet : https://www.pjrc.com/teensy/K66P144M180SF5RMV2.pdf
        pg 2189 for GPIO register data
        Teensy Interrupts Reference: https://www.pjrc.com/teensy/interrupts.html
        Teensy GPIO Register Mapping : https://forum.pjrc.com/archive/index.php/t-17532.html
        Motor Driver Tutorial: https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/
        PID library : https://playground.arduino.cc/Code/PIDLibrary/
        IMU datasheet  : https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
        IMU library    : https://github.com/ElectronicCats/mpu6050
        GPS library : https://github.com/SlashDevin/NeoGPS

        This program uses a GPS and encoder odometry to track a lat/long position using feedback linearization and PID controlled
        motors.

        Robert Whitney : rw429@cornell.edu : November 2020
*/


void setup() {
        Serial.begin(115200);   //Serial Monitor
        Serial1.begin(9600);    //GPS
        Serial2.begin(57600);   //Telemetry Radio

        //setup I2C bus using pins 7/8 (pins 18/19 used for encoder interrupts)
        Wire.begin(); Wire.setSCL(33); Wire.setSDA(34);

        //L298N Control Pins for motors 1 and 2
        pinMode(IN1, OUTPUT);  pinMode(IN2, OUTPUT);  pinMode(EN1, OUTPUT);
        pinMode(IN3, OUTPUT);  pinMode(IN4, OUTPUT);  pinMode(EN2, OUTPUT);
        pinMode(IN5, OUTPUT);  pinMode(IN6, OUTPUT);  pinMode(EN3, OUTPUT);
        pinMode(IN7, OUTPUT);  pinMode(IN8, OUTPUT);  pinMode(EN4, OUTPUT);

        //Encoder interrupts
        attachInterrupt(ENCD1_PINA, ENCD1_ISR, CHANGE);
        attachInterrupt(ENCD1_PINB, ENCD1_ISR, CHANGE);
        attachInterrupt(ENCD2_PINA, ENCD2_ISR, CHANGE);
        attachInterrupt(ENCD2_PINB, ENCD2_ISR, CHANGE);
        attachInterrupt(ENCD3_PINA, ENCD3_ISR, CHANGE);
        attachInterrupt(ENCD3_PINB, ENCD3_ISR, CHANGE);
        attachInterrupt(ENCD4_PINA, ENCD4_ISR, CHANGE);
        attachInterrupt(ENCD4_PINB, ENCD4_ISR, CHANGE);

        //Constrain PID limits
        ENCD1_PID.SetOutputLimits(-255, 255);   ENCD2_PID.SetOutputLimits(-255, 255);
        ENCD3_PID.SetOutputLimits(-255, 255);   ENCD4_PID.SetOutputLimits(-255, 255);

        //Start PID Control
        ENCD1_PID.SetMode(AUTOMATIC);   ENCD2_PID.SetMode(AUTOMATIC);
        ENCD3_PID.SetMode(AUTOMATIC);   ENCD4_PID.SetMode(AUTOMATIC);

        // initialize device & verify connection
        Serial.println("Initializing IMU...");
        accelgyro.initialize();
        Serial.println("Testing device connections...");
        Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

        //set the correct scaling (+/- 2g acc, +/- 500deg/s gyro)
        accelgyro.setFullScaleGyroRange(MPU6050_GYRO_FS_500);
        accelgyro.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);

        // use the code below to change accel/gyro offset values
        accelgyro.setXAccelOffset(-1345);
        accelgyro.setYAccelOffset(-4063);
        accelgyro.setZAccelOffset(1779);
        accelgyro.setXGyroOffset(90);
        accelgyro.setYGyroOffset(5);
        accelgyro.setZGyroOffset(13);
}

void loop() {
        //////// Sense ////////
        getMotorData();

        // read raw accel/gyro measurements from device [LSB]
        accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

        // GPS
        while (GPS.available(Serial1)) {
                FIX = GPS.read();
                isNewFix = true;
        }



        //////// Compute ////////
        //Euler angles from accelerometer, will be noisy but stable
        float rollAcc = atan2((float)ay , (float)az) * rad2deg;
        float pitchAcc = atan2((float) - ax , sqrt((float)ay * (float)ay + (float)az * (float)az)) * rad2deg;

        // Euler Angle Complementary Filter, stable and accurate
        float dT = (float)lastTime_IMU / 1000000; //[s]
        lastTime_IMU = 0;
        rollComp = alphaR * (rollComp + (float)gx * dT * gyrLSB2Dps) + (1 - alphaR) * rollAcc;
        pitchComp = alphaP * (pitchComp + (float)gy * dT * gyrLSB2Dps) + (1 - alphaP) * pitchAcc;

        // Localization
        double muNew[3], sigNew[9];
        const double covQR[2] = {measNse, prcssNse};
        const double odomData[2] = {(ENCD4.Vel + ENCD2.Vel)*dT / 2, (ENCD4.Vel - ENCD2.Vel)*dT  / (2 * trackWidth)};    // [deltaDist, deltaTheta]
        const double measGPS[3] = {(double)FIX.longitudeL(), (double)FIX.latitudeL(), (double)FIX.heading()};

        EKF_GPS(myMu, mySigma, odomData, measGPS, covQR, muNew, sigNew, isNewFix);

        //save updated mu and sigma into globals
        memcpy(myMu, muNew, sizeof(muNew));
        memcpy(mySigma, sigNew, sizeof(sigNew));

        //calculate desired global Vx and Vy
        double vBody[2], vGlobal[2] = {longRef - myMu[0], latRef - myMu[1]};

        //calculate local V and omega, then desired L & R wheel velocities
        feedbackLin(vGlobal, vBody);
        vel2_Ref = vBody[0] - trackWidth * vBody[1]; //left
        vel4_Ref = vBody[0] + trackWidth * vBody[1]; //right

        //Update encoder PIDs
        ENCD1_PID.Compute();  ENCD2_PID.Compute();
        ENCD3_PID.Compute();  ENCD4_PID.Compute();


        //////// Actuate ////////
        setMotor(MOTOR1, pos1_Cmd); setMotor(MOTOR2, vel2_Cmd);
        setMotor(MOTOR3, pos3_Cmd); setMotor(MOTOR4, vel4_Cmd);

        delay(1);
}
