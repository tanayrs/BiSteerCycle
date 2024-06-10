#include "TrivikramController.h"
#include <math.h>
//#include <filters.h>
//#include <filters_defs.h>

//Constructor
motorController::motorController(const int dirPin, const int motorPWMPin, const double kp, const double kd,bool wheel, double cutoff_freq, double sampling_time, double velKp, double velKi, double velKff){
  //Assigning values to variables
  // _cwPin = cwPin;
  // _ccwPin = ccwPin;
	_dirPin = dirPin;
	_motorPWMPin = motorPWMPin;
	_kp = kp;
	_kd = kd;
	_wheel = wheel;
	_sampling_time = sampling_time;
	_cutoff_freq = cutoff_freq;
	_velKp = velKp;
	_velKi = velKi;
	_velKff = velKff;

	//loopTimeConstSec = loopTimeConstant/1e6f;//TVC
	//for (int i =0; i<=200;i++){
	//	_timepoints[i] = -1*(loopTimeConstSec*200 - loopTimeConstSec*i);
	//}
	//_timepoints[0]  = -_timepoints[0];
	//_timepoints[200]= -_timepoints[200];
	
	//_cutoff_freq = cutoff_freq;
	//_sampling_time = sampling_time;

  //Setting PWM frequency and resolution - affects multiple pins, not just the set pin
  //See https://www.pjrc.com/teensy/td_pulse.html for more information regarding optimal frequencies and resolutions for various teensies
  //analogWriteFrequency(_motorPWMPin,14648.437); //Set PWM frequency to 14648.437 Hz for teensy 3.6
  analogWriteFrequency(_motorPWMPin,36621.09); //Set PWM frequency to 36621.09 Hz for teensy 4.1
  analogWriteResolution(12); // PWM value can take on a range from 0 to 4095
}

//Method to update the value of the error - assumes that the method parameters (reference and systemOutput) are between -180 and +180 degrees
void motorController::_updateError(double reference, double systemOutput){
  double error = reference - systemOutput;

  //If statements to correct for the case that abs(error) > 180
  //if (error > 180){
  //  error = error - 360;
  //}
  //else if (error < -180){
  //  error = error + 360;
  //}
  
  //Update error
  _previousError = _error;
  _error = error;
  //Update list of previous errors
  //_previousErrors.pop_front();
  //_previousErrors.push_back(_error);
}

//Linear regression to compute the slope of the error
//Formula found here: https://keisan.casio.com/exec/system/14059929550941
void motorController::_linearFit(){
    //Defining needed variables
  double yBar = 0; double xBar = 0; double sumXY = 0; double sumX2 = 0; double sumY2 = 0; double n = 0;//_previousErrors.size();

  //for (auto const& iterator: _previousErrors){
  //  double x = _timepoints[j];
  //  double y = iterator;
  //  j = j+1;

  //  //Updating sums
  //  yBar = yBar + y/n;
  //  xBar = xBar + x/n;
  //  sumXY = sumXY + x*y;
  //  sumX2 = sumX2 + x*x;
  //  sumY2 = sumY2 + y*y;
  //}

  double Sxx = sumX2 - n*xBar*xBar;
  double Syy = sumY2 - n*yBar*yBar;
  double Sxy = sumXY - n*xBar*yBar;
  
  //Computing slope of linear regression
  double slope = Sxy/Sxx;
  _linRegCoeff = slope;
	_errorROC = _linRegCoeff;

  if (Syy < 0.1){ //If statement to compensate for the situation where the error is constant
    double rSquared = 1;
    _rSquared = rSquared;
  }
  else{
    double rSquared = (Sxy*Sxy)/(Sxx*Syy);
    _rSquared = rSquared;
  }
  
}

//Function which updates the rate of change of the error variable. Applies recursive smoothing before doing so.
void motorController::_errorROCSmoothing(){
  //Computing smoothed r squared value
  double a1 = .15; double b1 = .85;
  _smoothedRSquared = a1*_rSquared + b1*_smoothedRSquared; //Recursively smoothed r squared value

  //Set the rate of change of the error to the value computed via linear regression if
  //the r squared value is high enough. Otherwise, set the rate of change of the error to zero
  double errorROC = 0;
  if (_smoothedRSquared > .9){
      errorROC = _linRegCoeff;
  } 
  
  double a2 = .8; double b2 = .2;
  _errorROC = a2*errorROC + b2*_errorROC; //Update the values of a and b for more or less smoothing. a+b must equal 1
}

//Function which computes the controller output voltage. Updates _outputVoltage and _feedForwardTerm.
//The feedForward parameter is not treated as a true feedForward term - instead of adding the parameter directly
//to the controllerOutputVoltage to obtain the voltage delivered to the motor, the sign of the feedForward term determines
//whether the magnitude of the output voltage is increased or decreased. i.e. if feedforward = 3, then 3V is added to the output voltage if the output voltage is positive,
// and -3V is added to the output voltage if the voltage is negative. Similarly, if feedForward = -3, then the magnitude of the output voltage is reduced by 3V.
//I set up the feedForward parameter in this way so that the magnitude of the output voltage could easily be changed without taking into account
//the direction of rotation of the motor.
double motorController::_computeOutputVoltage2(double feedForward){
  //Computing controller output
  _controllerOutputVoltage = _kp*_error + _kd*_errorROC;
//	double errorDeadband = 0.0;
//	if(_wheel){ //Modification with Ruina
//		if(fabs(_error) < errorDeadband){
//			controllerOutputVoltage = 0;
//		}
//		else if(_error >= errorDeadband){
//			controllerOutputVoltage = _kp*(_error-errorDeadband) + _kd*_errorROC;
//		}
//		else{
//			controllerOutputVoltage = _kp*(_error+errorDeadband) + _kd*_errorROC;
//		}
//	}

  //Assigning sign to the feedforward term
//  if (controllerOutputVoltage >= 0){
//    _feedForwardTerm = feedForward;
//  }
//  else {
//    _feedForwardTerm = -feedForward;
//  }

  //Computing output voltage of the controller + feedforward
//  double outputVoltage = controllerOutputVoltage + _feedForwardTerm;
  double outputVoltage = _saturateVoltage(_controllerOutputVoltage) ;
//	float maxVoltage = Battery_Voltage;
//  //Clipping outputVoltage to maxVoltage
//  if (outputVoltage > maxVoltage){
//    outputVoltage = maxVoltage;
//  }
//  else if (outputVoltage < -maxVoltage){
//    outputVoltage = -maxVoltage;
//  }

  //Updating _outputVoltage
  _outputVoltage = outputVoltage;
  return _outputVoltage;
}

//Function which computes the controller output voltage. Updates _outputVoltage and _feedForwardTerm.
//The feedForward parameter is not treated as a true feedForward term - instead of adding the parameter directly
//to the controllerOutputVoltage to obtain the voltage delivered to the motor, the sign of the feedForward term determines
//whether the magnitude of the output voltage is increased or decreased. i.e. if feedforward = 3, then 3V is added to the output voltage if the output voltage is positive,
// and -3V is added to the output voltage if the voltage is negative. Similarly, if feedForward = -3, then the magnitude of the output voltage is reduced by 3V.
//I set up the feedForward parameter in this way so that the magnitude of the output voltage could easily be changed without taking into account
//the direction of rotation of the motor.
void motorController::_computeOutputVoltage(double feedForward, double maxVoltage){
  //Computing controller output
  double controllerOutputVoltage = _kp*_error + _kd*_errorROC;
	double errorDeadband = 0.0;
	if(_wheel){ //Modification with Ruina
		if(fabs(_error) < errorDeadband){
			controllerOutputVoltage = 0;
		}
		else if(_error >= errorDeadband){
			controllerOutputVoltage = _kp*(_error-errorDeadband) + _kd*_errorROC;
		}
		else{
			controllerOutputVoltage = _kp*(_error+errorDeadband) + _kd*_errorROC;
		}
	}

  //Assigning sign to the feedforward term
  if (controllerOutputVoltage >= 0){
    _feedForwardTerm = feedForward;
  }
  else {
    _feedForwardTerm = -feedForward;
  }

  //Computing output voltage of the controller + feedforward
  double outputVoltage = controllerOutputVoltage + _feedForwardTerm;

  //Clipping outputVoltage to maxVoltage
  if (outputVoltage > maxVoltage){
    outputVoltage = maxVoltage;
  }
  else if (outputVoltage < -maxVoltage){
    outputVoltage = -maxVoltage;
  }

  //Updating _outputVoltage
  _outputVoltage = outputVoltage;
}


double motorController::_saturateVoltage(double voltage){
	if (voltage > _batteryVoltage){
		return _batteryVoltage;
	}else if( voltage < -_batteryVoltage){
		return -_batteryVoltage;
	}else{
		return voltage;
	}
	return 0;
}


//Method which calls analogWrite to set the pwm value for the motor
void motorController::_updatePWM(){
  //Compute ratio of desired outputVoltage to the maximum voltage
  double ratio = _outputVoltage / Battery_Voltage;

  //Obtain desired PWM value by multiplying ratio by 4095 (range of PWM values is 0 to 4095)
  double pwmValdouble = ratio*4095;
  //double pwmValdouble = ratio*255;
  //Cast pwm value to an int
  _pwmVal = (int)pwmValdouble;
  //analogWrite(_motorPWMPin,pwmVal);
}

//Method which calls analogWrite to set the pwm value for the motor
void motorController::_setPWM(double maxVoltage){
  //Compute ratio of desired outputVoltage to the maximum voltage
  double ratio = _outputVoltage / maxVoltage;

  //If ratio is negative, make positive
  if (ratio < 0){
    ratio = -ratio;
  }

  //Obtain desired PWM value by multiplying ratio by 4095 (range of PWM values is 0 to 4095)
  //double pwmValdouble = ratio*4095;
  double pwmValdouble = ratio*4095;

  //Cast pwm value to an int
  int pwmVal = (int)pwmValdouble;

  analogWrite(_motorPWMPin,pwmVal);
}

//Method which changes the direction of motor rotation depending upon the sign of _outputVoltage
void motorController::_setDirection(){
  if (_outputVoltage > 0){
   // digitalWriteFast(_cwPin,HIGH);
   // digitalWriteFast(_ccwPin,LOW);
  }
  else if (_outputVoltage < 0){
   // digitalWriteFast(_cwPin,LOW);
   // digitalWriteFast(_ccwPin,HIGH);
  }
}


void motorController::_updateErrorROC(){
	double errorROC2 = (_error - _previousError)/_sampling_time;
	//double filteredErrorROC = f_error.filterIn(errorROC2);
	//double filteredErrorROC = _filterLPF(_errorROC, errorROC2);
	//double filteredErrorROC = _LPF_Error(errorROC2);
	double filteredErrorROC = (errorROC2);
	 _errorROC = filteredErrorROC;
	//return _errorROC = errorROC2; //filteredErrorROC;
	//return  errorROC2; 
}


double motorController::_LPF_Error(double newROC){
	double timeConstant = 1/_cutoff_freq;
	double alpha = (timeConstant)/(timeConstant + _sampling_time);
	return alpha*_errorROC + (1-alpha)*newROC;
}


//Method to be called in an interval timer to run the controller
int motorController::positionPDControl(double reference, double systemOutput){
	_currentPosition = systemOutput;
	
  _updateError(reference, systemOutput); //Updates _error, updates _previousErrors
  _updateErrorROC();
  _computeOutputVoltage2(_feedForwardTerm); //Computes the desired controller output voltage and updates _feedForwardTerm and _outputVoltage
  _previousPosition = _currentPosition;
  _updatePWM();
  return PWM();
}
//Method to be called in an interval timer to run the controller
//void motorController::updateOutput(double reference, double systemOutput, double maxVoltage, double feedForward){
//  _updateError(reference, systemOutput); //Updates _error, updates _previousErrors
//  //_linearFit(); //Applies linear regression to the error vs time data
//  //_errorROCSmoothing(); //Applies filtering and recursive smoothing to the rate of change of the error. Updates _errorROC
//  _computeOutputVoltage(feedForward, maxVoltage); //Computes the desired controller output voltage and updates _feedForwardTerm and _outputVoltage
//  _setPWM(maxVoltage); //Sets the appropriate pwm value for the motor based upon the desired output voltage
//  _setDirection();
//}

//Getter to return error
double motorController::error(){
  return _error;
}

//Getter to return rate of change of error
double motorController::errorROC(){
  return _errorROC;
}

//Getter to return the controller output voltage after saturation
double motorController::outputVoltage(){
  return _outputVoltage;
}

// Getter to return the unsaturated voltage calculated by the motor controller
double motorController::controllerVoltage(){
	return _controllerOutputVoltage;
}

//Getter to return the r squared value for the linear regression used to compute the rate of change of the error
double motorController::errorR2(){
  return _rSquared;
}

//Getter to return the smoothed r squared value
double motorController::smoothedErrorR2(){
  return _smoothedRSquared;
}


//Getter to return the feedforward value
double motorController::feedForward(){
  return _feedForwardTerm;
}

//Getter to return the PWM value
int motorController::PWM(){
  return _pwmVal;
}


int motorController::velocityPIControl(double omega, double omegaRef){
	_omegaError = omega - omegaRef;
	_omegaErrInteg += _omegaError*_sampling_time;
	_controllerOutputVoltage = _velKff*omegaRef + _velKp*_omegaError + _velKi*_omegaErrInteg ; //PI + FF Only
	_outputVoltage = _saturateVoltage(_controllerOutputVoltage);
	_updatePWM();
	return PWM();
}


double motorController::omegaError(){
  return _omegaError;
}


double motorController::omegaErrInteg(){
  return _omegaErrInteg;
}



