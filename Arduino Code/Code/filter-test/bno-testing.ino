void startup_routine_bno(){
                Serial.println("Orientation Sensor Test"); Serial.println("");

        /* Initialise the sensor */
        if(!bno.begin()){
                /* There was a problem detecting the BNO055 ... check your connections */
                Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
                while(1);
        }

        delay(1000);
        bno.setExtCrystalUse(true);
}

// Defining Sensor Object //
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28, &Wire);

// Defining Variables for Derivatives, Angle, and Constants //
double previous_roll, elapsedTimeIMU, IMUFilterConstant,gyroAngleX, accelAngle,roll;
double IMUTimeConstant = 6.0;
float kalRoll = 0;
elapsedMicros IMUTimeMicros;

// Defining State Variables //
double phi, phi_dot;

// Defining Kalman Filter Object //
// Our Values: 0.005, 0, 0,1 //
// Library Values: 0.001,0.003,0.03 //
KalmanFilter kalmanX(0.001, 0.003, 0.03);  //(Q_angle, Q_bais, R) //

/* Calculate Angles from BNO-055 Sensor */
void calculate_bno_angle() {
        // Finding Sensor Readings //
        sensors_event_t event;
        bno.getEvent(&event);
        
        // Updating Roll and Phi //
        previous_roll = roll;
        roll = event.orientation.z;
        phi = roll;

        // Printing Angle Values to Serial Monitor //
        Serial.print(event.orientation.x); Serial.print(" ");
        Serial.print(event.orientation.y); Serial.print(" ");
        Serial.print(event.orientation.z); Serial.print(" ");
        Serial.println("");
}

/* Calculate Angles from BNO-055 Sensor using a Kalman Filter */
void calculate_bno_angle_kalman() {
        // Finding Sensor Readings //
        sensors_event_t a, g;
        bno.getEvent( & a, Adafruit_BNO055::VECTOR_ACCELEROMETER);
        bno.getEvent( & g, Adafruit_BNO055::VECTOR_GYROSCOPE);

        // Calculating Angle from Accelerometer //
        float ax = a.acceleration.x;
        float ay = a.acceleration.y;
        float az = a.acceleration.z;
        float acc_angle_x = 180 * atan2(ay, sqrt(ax*ax + az*az))/PI;     

        // Passing Angle and Angle Rate to Kalman Filter Object //
        float kalX = (kalmanX.update(acc_angle_x, g.gyro.x * 180/PI));
        
        phi = kalX;
        phi_dot = g.gyro.x;
}

/* Calibration of BNO-055 */
void gyro_bias(){
        sensors_event_t a, g, event;
        float x_error = 0;
        float y_error = 0; 
        float z_error = 0;
        for (int i = 0; i <10000; i++) {
            bno.getEvent( &g, Adafruit_BNO055::VECTOR_GYROSCOPE);
            x_error += g.gyro.x;
            y_error += g.gyro.y;
            z_error += g.gyro.z;
        }
        x_error = x_error/10000;
        y_error = y_error/10000;
        z_error = z_error/10000;

        Serial.print("X bias: "); Serial.print(x_error); Serial.println("");
        Serial.print("Y bias: "); Serial.print(y_error); Serial.println("");
        Serial.print("Z bias: "); Serial.print(z_error); Serial.println("");
}

void filter_testing() {
        // Finding Sensor Readings //
        sensors_event_t a, g, event;
        bno.getEvent( & a, Adafruit_BNO055::VECTOR_ACCELEROMETER);
        bno.getEvent( & g, Adafruit_BNO055::VECTOR_GYROSCOPE);
        bno.getEvent(&event);

        // Calculating Angle from Accelerometer //
        float ax = a.acceleration.x;
        float ay = a.acceleration.y;
        float az = a.acceleration.z;
        float acc_angle_y = -180 * atan2(ax, sqrt(ay*ay + az*az))/PI;     

        // Passing Angle and Angle Rate to Kalman Filter Object //
        float kalY = (kalmanX.update(acc_angle_y, g.gyro.y * 180/PI));
        
        phi = kalY;
        phi_dot = g.gyro.y;

        // Printing Accelerometer, Complimentary Filter, and Kalman Filter Angles //
        Serial.print(millis()); Serial.print(" ");
        Serial.print(acc_angle_y); Serial.print(" ");
        Serial.print(-event.orientation.y); Serial.print(" ");
        Serial.print(kalY); Serial.println("");

}
