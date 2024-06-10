/**
* BNO-055 IMU Test Code from: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
* Modified to Plot Values on Serial Plotter as Compared to Printing on Serial Monitor.
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <elapsedMillis.h>
#include <KalmanFilter.h> // Repo: https://github.com/jarzebski/Arduino-KalmanFilter/tree/master //
#include <Adafruit_Sensor.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28, &Wire);

sensors_event_t a, g, temp;
float ax1, ay1, az1;
float gx1, gy1, gz1;
double previous_roll, elapsedTimeIMU, IMUFilterConstant,gyroAngleX, accelAngle,roll;
double IMUTimeConstant = 6.0;
elapsedMicros IMUTimeMicros;
float kalRoll = 0;
double phi, phi_dot;
KalmanFilter kalmanX(0.005, 0, 0.1);  //(Q_angle, Q_bais, R) //
KalmanFilter kalmanY(0.005, 0, 0.1);  //(Q_angle, Q_bais, R) //
//KalmanFilter kalmanZ(0.0005, 0.005, 0.1);  //(Q_angle, Q_bais, R) //

/* Finds Pitch From Accelerometer -> Returns in Degrees */
float accelero_angle() {
        return atan2(ay1, -az1) * 180.0 / PI;
}

/* Calculate Angles from BNO-055 Sensor */
void calculate_bno_angle() {
        sensors_event_t event;
        bno.getEvent(&event);
        previous_roll = roll;
        roll = event.orientation.z;
        phi = roll;
        Serial.print(event.orientation.x); Serial.print(" ");
        Serial.print(event.orientation.y); Serial.print(" ");
        Serial.print(event.orientation.z); Serial.print(" ");
        Serial.println("");
        //bno.getEvent(&event, Adafruit_BNO055::VECTOR_GYROSCOPE);
        //phi_dot = event.gyro.z;
}

/* Calculate Angles from BNO-055 Sensor using a Complimentary Filter */
void calculate_bno_angle_compfilter() {
        bno.getEvent( &a, Adafruit_BNO055::VECTOR_ACCELEROMETER);
        bno.getEvent( &g, Adafruit_BNO055::VECTOR_GYROSCOPE);

        elapsedTimeIMU = IMUTimeMicros / 1000.0;
        IMUTimeMicros = 0;
        IMUFilterConstant = IMUTimeConstant / (IMUTimeConstant + (elapsedTimeIMU / 1000.0));

        ax1 = a.acceleration.x;
        ay1 = a.acceleration.y;
        az1 = a.acceleration.z;
        gx1 = (g.gyro.x) * 180.0 / PI; // Angle in degrees //

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
        float acc_angle_y = 180 * atan2(ax, sqrt(ay*ay + az*az))/PI;
        float acc_angle_x = 180 * atan2(ay, sqrt(ax*ax + az*az))/PI;     

        // passing angle and angular rate to kalman filter for x, y and z
        float kalX = (kalmanX.update(acc_angle_x, g.gyro.x * 180/PI));
        float kalY = (kalmanY.update(acc_angle_y, g.gyro.y * 180/PI));
        
        phi = kalX;
        phi_dot = g.gyro.x;

        Serial.print(acc_angle_x); Serial.print(" ");
        Serial.print(acc_angle_y); Serial.print(" ");
        Serial.print(kalX); Serial.print(" ");
        Serial.print(kalY); Serial.print(" ");
        Serial.println("");

        // Serial.print(g.gyro.x); Serial.print(" ");
        // Serial.print(g.gyro.y); Serial.print(" ");
        // Serial.print(g.gyro.z); Serial.print(" ");
        // Serial.println("");
}

void setup(void) 
{
        Serial.begin(9600);
        Serial.println("Orientation Sensor Test"); Serial.println("");

        /* Initialise the sensor */
        if(!bno.begin())
        {
                /* There was a problem detecting the BNO055 ... check your connections */
                Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
                while(1);
        }

        delay(1000);
        bno.setExtCrystalUse(true);

        // Calculating bias from gyroscope readings
        // gyro_bias();
}

void print_state_vars(){
        Serial.print(phi); Serial.print(" ");
        Serial.print(phi_dot); Serial.print(" ");
}

void gyro_bias(){
        float x_error = 0;
        float y_error = 0; 
        float z_error = 0;
        for (int i = 0; i <10000; i++)
        {
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


void loop(void) {
        // calculate_bno_angle();
        // print_state_vars();
        // calculate_bno_angle_compfilter();
        // print_state_vars();
        calculate_bno_angle_kalman();
        // print_state_vars();
        // Serial.println("");
        delay(10);
}
