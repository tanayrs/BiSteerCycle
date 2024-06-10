#ifndef PI
#define PI 3.14159265
#endif

#ifndef motorEnc
#define motorEnc

#include "Arduino.h"
//#include <list>
#include "math.h"

class EncoderDataProcessor{
  public:
    //Constructor
    EncoderDataProcessor(double pulsesPerRev,double playInDegrees,bool wheel,bool front, double cutoff_freq, double sampling_time); //"Wheel" and "front" correspond to wheel vs steering motors and front vs rear motor

    //Public methods
    long ticks(); //Returns the value of _encTicks
    double degreesAccumulated(); //Returns the total number of degrees through which the encoder has rotated since begin or reset
    double degreesPosition(); //Returns the orientation of the encoder between -180 and +180 degrees. The zero point is defined using begin or reset + reseting the encoder
    double radianPosition(); //Returns the orientation of the encoder between -180 and +180 degrees. The zero point is defined using begin or reset + reseting the encoder
    double speed(); //Returns an estimate of the motor angular speed in rad/s
    //double acceleration(); //Returns an estimate of the angular acceleration - Commented out because the acceleration estimate is poor
    void update(long ticks,double steerAccumulatedTicks,double steerTicksOffset); //To be called within the main program in an IntervalTimer every 1 ms - Updates values
	//void reset(); //Resets tick count, speed, ticksLists, coeffs array, and _previousSpeeds list
    double adjustedDegreesPosition(); //Returns the orientation of the encoder between -180 and +180 degrees. The zero point is defined using begin or reset + reseting the encoder
    //double adjustedDegreesPosition(); //Returns the orientation of the encoder between -180 and +180 degrees. The zero point is defined using begin or reset + reseting the encoder
    double adjustedRadianPosition(); //Returns the orientation of the encoder between -180 and +180 degrees. The zero point is defined using begin or reset + reseting the encoder
    
	double bevelGearRatio;
	double steerPPR;
  private: 
    //Value to store the number of counted encoder ticks
    long _encTicks = 0;

	//Variable to store encoder ticks/degrees adjusted to take play into account
	double _adjustedEncTicks = 0;
	double _adjustedWheelDeg = 0;

    //Variables to store current velocity and acceleration
    double _speed = 0;
    //double _acceleration = 0;

    //Ticks per revolution of encoder
    double _ticksPerRev;

	//Width of the deadband between the motor and the output shaft
	double _playInDegrees;

	//Deadband range
	double _deadBandUpper;
	double _deadBandLower;

	//Variables to identify the motor
	bool _wheel;
	bool _front;


    //Definition of pi
    const double _pi = 3.14159265;
    
    //Lists and an array for computing angular velocity
    //const double _timepoints[21] = { -0.0200,   -0.0190, -0.0180,   -0.0170,   -0.0160,   -0.0150,   -0.0140,   -0.0130,   -0.0120,   -0.0110,
//    -0.0100,   -0.0090,   -0.0080, -0.0070,   -0.0060,   -0.0050,   -0.0040,   -0.0030,   -0.0020,   -0.0010,         0};

    //std::list<double> _encTicksList {std::list<double>(21,0)};
	//std::list<double> _wheelDegList {std::list<double>(21,0)};
    //std::list<double> _zeroedEncTicksList {std::list<double>(21,0)};
	//std::list<double> _zeroedWheelDegList {std::list<double>(21,0)};

    //Array to store quadratic regression coefficients
    //double _coeffs[3] = {0.0, 0.0, 0.0};

    //List and array to store previous speeds and timepoints at which they were acquired - used for computing acceleration and for recursive smoothing of speed
    //const double _speedTimepoints[10] = {-.002,-.001,0};
    //std::list<double> _previousSpeeds {std::list<double>(3,0)};

    //Private methods
    //void _updateTicks(); //Reads encoder object ticks value - not used anymore
    //void _updateEncLists(); //Update lists for computing angular speed
    //void _quadraticFit(); //Fit quadratic expression to position data stored in lists, updates _speed
    //void _linearFit(); //Fit linear expression to speed data stored in _previousSpeeds list, updates _acceleration
	void _updateEncListsPlay();
	double _computeCoupledWheelRotation(double steerAccumulatedTicks, double steerTicksOffset); //Computes rotation of the wheel in degrees taking the bevel gear coupling into account
	void _updateEncListsCouplingAndPlay(double steerAccumulatedTicks,double steerTicksOffset); //Updates the _wheelDegList and _zeroedWheelDegList used for wheel speed calculation
	void _updateSpeed();
	////void _updateAccel();
	double LPF_speed(double newSpeed);
	double _sampling_time; //In Seconds
	double _cutoff_freq; //In Hertz
	long _previousAdjEncTicks=0;
	double _previousAdjWheelDeg=0;
};





























#endif
