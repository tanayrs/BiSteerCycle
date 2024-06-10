#ifndef Battery_Voltage
#define Battery_Voltage 12.0
#endif

#ifndef loopTimeConstant 
#define loopTimeConstSec 0.002 
#endif

#ifndef loopTimeConstant
#define loopTimeConstant 2000
#endif

#ifndef motorPositionController
#define motorPositionController

#include "Arduino.h"
//#include <list>
#include <filters.h>
#include <filters_defs.h>
#include <CytronMotorDriver.h>

class motorController{
  public:

    //Constructor
    //Constructor assigns values to variables and also sets pwm frequency and resolution. PWM frequency and resolution are
    //optimized for teensy 4.1. These values may not work for other teensy versions
    motorController(const int dirPin, const int motorPWMPin, const double kp, const double kd,bool wheel, double cutoff_freq, double sampling_time, double velKp, double velKi, double velKff);
	
	
 
	//float loopTimeConstSec =0;
    //Public methods
    double error(); //Returns the difference between the reference and the current position value in degrees
    double errorROC(); //Returns the rate of change of the error
    double outputVoltage(); //Returns the output voltage of the controller
    double errorR2(); //Returns the r squared value for the linear regression of the error
    double smoothedErrorR2(); //Returns the smoothed r squared value
    double feedForward(); //Returns the current feedforward value
    //Takes in a reference, the current system output, a feedfoward term (not a true feedforward term! See below comment) and the voltage available to motor
    //Sets motor pins to controller output
    //This method should go in an IntervalTimer which triggers every 1000 microseconds
    //Feedforward term is not added directly to the controller voltage - instead, the sign of the feedForward parameter indicates what happens to the 
    //magnitude of the output voltage. i.e. if feedforward = 3, then 3V is added to the output voltage if the output voltage is positive, and -3V is added
    //to the output voltage if the voltage is negative. Similarly, if feedForward = -3, then the magnitude of the output voltage is reduced by 3V.
    //I set up the feedForward parameter in this way so that the magnitude of the output voltage could easily be changed without taking into account
    //the direction of rotation of the motor.
    //void updateOutput(double reference, double systemOutput, double maxVoltage, double feedForward = 0);
    int positionPDControl(double reference, double systemOutput);//TVC
	//double velocity(); //TVC - finds the fi
    int PWM(void); //TVC Returns the PWM value
    double controllerVoltage(void); //TVC Returns the controller generated unsaturated voltage
    int velocityPIControl(double omega, double omegaRef); //TVC Returns the controller generated saturated voltage for PI velocity control;
	double omegaError();//TVC Getter
	double omegaErrInteg();//TVC Getter
	//friend class Filter;
	//Filter f_error;
	//Filter f_vel;
	//double ROC_LPF();//TVC - returns the smoothed velocity of the motor;
//	void setVoltageCytron();// TVC - use the calculated PWM and Dir to set the cytron motor driver
	//int PWM();//TVC - outputs the PWM which we have to supply to a MD
	//int saturateVoltage(float Voltage);//TVC - Saturates wrt battery voltage

  private:
    //Private variables
	double _currentPosition =0;//TVC Degrees
	double _pwmVal=0;//TVC Degrees
	float _sampling_time=0.002; //Seconds
	float _cutoff_freq=20; //Hz
	double _previousPosition=0;//TVC Degrees
	float _batteryVoltage = Battery_Voltage;//TVC Volts
	double _timepoints[201]; //TVC
	double _controllerOutputVoltage; //TVC
    double _error = 0; //Current difference between reference and actual position value in degrees
    double _errorROC = 0; //Current rate of change of the error - DPS
    double _outputVoltage = 0; //Current average output voltage - Volts
    int _dirPin;
    int _cwPin;
    int _ccwPin;
    int _motorPWMPin;
	bool _wheel; //Indicates whether the motor controller is for one of the wheel motors
    double _kp; //Proportional gain
    double _kd; //Derivative gain
    double _linRegCoeff = 0; //Slope of line obtained from linear regression of error vs time - gives rate of change of error
    double _rSquared = 0; //_rSquared value of most recent linear regression
    double _smoothedRSquared = 0; //Recursively smoothed r squared value
    double _feedForwardTerm = 0; //Storage variable to allow the values of the feedforward inputs to be logged
    double _velKp;//TVC
    double _velKi;//TVC
    double _velKff;//TVC
    double _omegaError;//TVC
    double _omegaErrInteg;//TVC
    
    //Timepoints in seconds
	//std::list<double> _previousErrors {std::list<double>(201,0)};
	double _previousError =0;


    //Private methods
	double _saturateVoltage(double voltage);
	double _LPF_Error(double newROC); //TVC - Applies a recursive smoothing filter, gives result in DPS
	void _updateErrorROC();// TVC - finds the filtered Rate of Change of error of the motor in DPS.
    void _updateError(double reference, double systemOutput); //Updates _error, updates _previousErrors
    void _linearFit(); //Fits a line to previous errors vs time. Updates _linRegCoeff and _rSquared
    void _errorROCSmoothing(); //Applies recursive smoothing to generate a smoother stream of _errorSlopes. Updates _errorSlope
    void _computeOutputVoltage(double feedForward, double maxVoltage); //Computes the desired controller output voltage and updates _outputVoltage
    double _computeOutputVoltage2(double feedForward); //TVC Computes the desired controller output voltage and updates _outputVoltage
    void _setPWM(double maxVoltage); //Sets the appropriate pwm value for the motor based upon the desired output voltage
    void _updatePWM(); //Sets the appropriate pwm value for the motor based upon the desired output voltage
    void _setDirection(); //Changes the direction of motor rotation based upon the sign of _outputVoltage
    //double _timepoints[201] = {0.2000,-0.1990,-0.1980,-0.1970,-0.1960,-0.1950,-0.1940,-0.1930,-0.1920,-0.1910,-0.1900,-0.1890,-0.1880,-0.1870,-0.1860,-0.1850,-0.1840,-0.1830,-0.1820,-0.1810,-0.1800,-0.1790,-0.1780,-0.1770,-0.1760,-0.1750,-0.1740,-0.1730,-0.1720,-0.1710,-0.1700,-0.1690,-0.1680,-0.1670,-0.1660,-0.1650,-0.1640,-0.1630,-0.1620,-0.1610,-0.1600,-0.1590,-0.1580,-0.1570,-0.1560,-0.1550,-0.1540,-0.1530,-0.1520,-0.1510,-0.1500,-0.1490,-0.1480,-0.1470,-0.1460,-0.1450,-0.1440,-0.1430,-0.1420,-0.1410,-0.1400,-0.1390,-0.1380,-0.1370,-0.1360,-0.1350,-0.1340,-0.1330,-0.1320,-0.1310,-0.1300,-0.1290,-0.1280,-0.1270,-0.1260,-0.1250,-0.1240,-0.1230,-0.1220,-0.1210,-0.1200,-0.1190,-0.1180,-0.1170,-0.1160,-0.1150,-0.1140,-0.1130,-0.1120,-0.1110,-0.1100,-0.1090,-0.1080,-0.1070,-0.1060,-0.1050,-0.1040,-0.1030,-0.1020,-0.1010,-0.1000,-0.0990,-0.0980,-0.0970,-0.0960,-0.0950,-0.0940,-0.0930,-0.0920,-0.0910,-0.0900,-0.0890,-0.0880,-0.0870,-0.0860,-0.0850,-0.0840,-0.0830,-0.0820,-0.0810,-0.0800,-0.0790,-0.0780,-0.0770,-0.0760,-0.0750,-0.0740,-0.0730,-0.0720,-0.0710,-0.0700,-0.0690,-0.0680,-0.0670,-0.0660,-0.0650,-0.0640,-0.0630,-0.0620,-0.0610,-0.0600,-0.0590,-0.0580,-0.0570,-0.0560,-0.0550,-0.0540,-0.0530,-0.0520,-0.0510,-0.0500,-0.0490,-0.0480,-0.0470,-0.0460,-0.0450,-0.0440,-0.0430,-0.0420,-0.0410,-0.0400,-0.0390,-0.0380,-0.0370,-0.0360,-0.0350,-0.0340,-0.0330,-0.0320,-0.0310,-0.0300,-0.0290,-0.0280,-0.0270,-0.0260,-0.0250,-0.0240,-0.0230,-0.0220,-0.0210,-0.0200,-0.0190,-0.0180,-0.0170,-0.0160,-0.0150,-0.0140,-0.0130,-0.0120,-0.0110,-0.0100,-0.0090,-0.0080,-0.0070,-0.0060,-0.0050,-0.0040,-0.0030,-0.0020,-0.0010,0};
};

#endif
