#include "TrivikramEncoder.h"

//Constructor
EncoderDataProcessor::EncoderDataProcessor(double pulsesPerRev,double playInDegrees,bool wheel,bool front, double cutoff_freq, double sampling_time){
	_ticksPerRev = 4*pulsesPerRev; //Encoder object outputs 4 ticks per encoder pulse
	_playInDegrees = playInDegrees;
	if(wheel){
	_deadBandUpper = playInDegrees/2.0; //Deadband is defined in terms of degrees for wheel (to take bevel gear coupling into account)
	_deadBandLower = -playInDegrees/2.0;
	}
	else{
	_deadBandUpper = (playInDegrees/2.0)*_ticksPerRev/(360.0); //Deadband is defined in terms of ticks for steering
	_deadBandLower = -(playInDegrees/2.0)*_ticksPerRev/(360.0);
	}
	_wheel = wheel; //Wheel or steering encoder
	_front = front; //Front or rear motor
	//For more information about how this works, see: https://www.pjrc.com/teensy/td_libs_Encoder.html
	
	bevelGearRatio = 1.0;
	steerPPR = 2264;
	_cutoff_freq = cutoff_freq;
	_sampling_time = sampling_time;
}


//Updates speed estimate - should be called in an intervaltimer (set to 1 ms) - can update acceleration as well, commented this out
void EncoderDataProcessor::update(long ticks,double steerAccumulatedTicks,double steerTicksOffset){
  _encTicks = ticks;
	if(_wheel){
		_updateEncListsCouplingAndPlay(steerAccumulatedTicks,steerTicksOffset);
	}
	else{
		_updateEncListsPlay();
	}
	_updateSpeed();
	//_updateAccel();
  //_quadraticFit();
  //_linearFit();
}

//Function which converts wheel and steering angle rotations to rotations of the wheel in degrees
//steerTicksOffset is the number of encoder ticks of the steering motor immediately following the initial routine
double EncoderDataProcessor::_computeCoupledWheelRotation(double steerAccumulatedTicks, double steerTicksOffset){
  //Converting wheel and encoder ticks to rotations in degrees
	double bevelGearRatio = 1.0;
	double sprocketRatio = 1.0;//40.0/26.0;
	double steerPPR = 8540/4;
	double wheelTicksToDegrees = degreesAccumulated()/bevelGearRatio;
	
	double steerTicksToDegrees = 360.0*(steerAccumulatedTicks - steerTicksOffset)/(bevelGearRatio*steerPPR*sprocketRatio); 
	
	//Combining wheel and steering data
	double combinedRotationDeg;
	if(_front){
		combinedRotationDeg = wheelTicksToDegrees - steerTicksToDegrees;
	}
	else{
		combinedRotationDeg = wheelTicksToDegrees + steerTicksToDegrees;
	}

	return combinedRotationDeg;
}

//Update encoder lists method taking play and bevel gear coupling into account
void EncoderDataProcessor::_updateEncListsCouplingAndPlay(double steerAccumulatedTicks,double steerTicksOffset){
	//Computing rotation of wheel
	double wheelDegrees = _computeCoupledWheelRotation(steerAccumulatedTicks,steerTicksOffset);

  //Adjusting deadband and updating encoder ticks
  if(wheelDegrees > _deadBandUpper){
		_adjustedWheelDeg = _adjustedWheelDeg + (wheelDegrees - _deadBandUpper);
		_deadBandUpper = wheelDegrees;
		_deadBandLower = _deadBandUpper - _playInDegrees;
  }
  else if(wheelDegrees < _deadBandLower){
		_adjustedWheelDeg = _adjustedWheelDeg + (wheelDegrees - _deadBandLower);
		_deadBandLower = wheelDegrees;
		_deadBandUpper = _deadBandLower + _playInDegrees;
  }
//  //Remove first item from list
//  _wheelDegList.pop_front();
//  //Append encoder ticks value to end of list
//  _wheelDegList.push_back(_adjustedWheelDeg);
//
//  //Clear zeroedWheelDegList
//  _zeroedWheelDegList = {};
//
//  //Obtain value of first item in wheelDegList
//  double firstVal = _wheelDegList.front();
//
//  //Append data in wheelDegList to zeroedWheelDegList while subtracting away value of first term
//  for (auto const& iterator: _wheelDegList){
//    double value = iterator - firstVal;
//    _zeroedWheelDegList.push_back(value);
//  }
}

//Update encoder lists method taking play into account
void EncoderDataProcessor::_updateEncListsPlay(){
  //Adjusting deadband and updating encoder ticks
  if(_encTicks > _deadBandUpper){
		_adjustedEncTicks = _adjustedEncTicks + ((double)_encTicks - _deadBandUpper);
		_deadBandUpper = (double)_encTicks;
		_deadBandLower = _deadBandUpper - _playInDegrees*_ticksPerRev/360.0;
  }
  else if(_encTicks < _deadBandLower){
		_adjustedEncTicks = _adjustedEncTicks + ((double)_encTicks - _deadBandLower);
		_deadBandLower = (double)_encTicks;
		_deadBandUpper = _deadBandLower + _playInDegrees*_ticksPerRev/360.0;
  }
//  //Remove first item from list
//  _encTicksList.pop_front();
//  //Append encoder ticks value to end of list
//  _encTicksList.push_back(_adjustedEncTicks);
//
//  //Clear zeroedEncTicksList
//  _zeroedEncTicksList = {};
//
//  //Obtain value of first item in encTicksList
//  double firstVal = _encTicksList.front();
//
//  //Append data in encTicksList to zeroedEncTicksList while subtracting away value of first term
//  for (auto const& iterator: _encTicksList){
//    double value = iterator - firstVal;
//    _zeroedEncTicksList.push_back(value);
//  }
}

//Quadratic fit method
//Defines function to compute quadratic expression coefficients using least squares regression
//The method that I am using for regression can be found here: https://keisan.casio.com/exec/system/14059932254941
//Also see MATLAB file a1_21_21_Velocity_from_encoder_position_data_matrix.m - tested this quadratic regression algorithm there
//void EncoderDataProcessor::_quadraticFit(){
//	//Specifying which list to use
//	std::list<double> regList;
//	if(_wheel){
//		regList = _zeroedWheelDegList;
//	}
//	else{
//		regList = _zeroedEncTicksList;
//	}
//
//  //Initializing terms which are needed for regression
//  double xbar = 0; double x2bar = 0; double ybar = 0; double sumXsquared = 0; double sumXcubed = 0; double sumXfourth = 0; double sumXY = 0; double sumX2Y = 0;
//  double Sxx = 0; double Sxy = 0; double Sxx2 = 0; double Sx2x2 = 0; double Sx2y = 0; double n = regList.size();
//
//  //Loop to iterate through array/list to assign the proper values to the first line of above initialized variables
//  int j = 0; //Dummy variable
//  for (auto const& iterator: regList){
//    double y = iterator;
//    double x = _timepoints[j];
//    j = j+1;
//
//    xbar = xbar + x/n;
//    x2bar = x2bar + x*x/n;
//    ybar = ybar + y/n;
//    sumXsquared = sumXsquared + x*x;
//    sumXcubed = sumXcubed + x*x*x;
//    sumXfourth = sumXfourth + x*x*x*x;
//    sumXY = sumXY + x*y;
//    sumX2Y = sumX2Y + x*x*y;
//  }
//
//  //Assigning values to Sxx,Sxy,etc.
//  Sxx = sumXsquared - n*xbar*xbar;
//  Sxy = sumXY - n*xbar*ybar;
//  Sxx2 = sumXcubed - n*xbar*x2bar;
//  Sx2x2 = sumXfourth - n*x2bar*x2bar;
//  Sx2y = sumX2Y - n*x2bar*ybar;
//
//  //Generating coefficients for regression of the form y = Ax^2 + Bx + C
//  double A = (Sx2y*Sxx-Sxy*Sxx2)/(Sxx*Sx2x2 - Sxx2*Sxx2);
//  double B = (Sxy*Sx2x2 - Sx2y*Sxx2)/(Sxx*Sx2x2-Sxx2*Sxx2);
//  double C = ybar - B*xbar - A*x2bar;
//
//  //Updating coeffs array
//  _coeffs[0] = A;
//  _coeffs[1] = B;
//  _coeffs[2] = C;
//
//	double angularSpeed;
//	if(_wheel){
//		double degsSpeed = B; //Angular speed in degrees/s
//		angularSpeed = _pi*degsSpeed/180.0; //Angular speed in rad/s
//	}
//	else{
//		//Computing angular speed in ticks per second - elapsed time must be in seconds
//		double ticksSpeed = B;
//		//Converting angular speed to rad/s
//		angularSpeed = 2*_pi*ticksSpeed / _ticksPerRev;
//	}
//  
//  //Updating _speed with recursive smoothing
//  double previousSpeed = _previousSpeeds.back();
//  _speed = 0.25*angularSpeed + 0.75*previousSpeed;
//
//  //Updating _previousSpeeds List
//  _previousSpeeds.pop_front();
//  _previousSpeeds.push_back(_speed);
//}

//Linear fit method for computing acceleration - Commented out because it does not work well
/*void EncoderDataProcessor::_linearFit(){
  //Defining needed variables
  double sumY = 0; double sumX = 0; double sumXY = 0; double sumX2 = 0; double n = _previousSpeeds.size();

  int j = 0; //Dummy variable
  for (auto const& iterator: _previousSpeeds){
    double x = _speedTimepoints[j];
    double y = iterator;
    j = j+1;

    //Updating sums
    sumY = sumY + y;
    sumX = sumX + x;
    sumXY = sumXY + x*y;
    sumX2 = sumX2 + x*x;
  }

  //Computing slope of linear regression
  double slopeNumerator = n*sumXY - sumX*sumY;
  double slopeDenominator = n*sumX2 - sumX*sumX;
  double slope = slopeNumerator/slopeDenominator;

  //Updating value of acceleration with recursive smoothing
  _acceleration = .3*slope + 0.7*_acceleration;
}*/



//Update encoder lists method - Doesn't take play into account
/*void EncoderDataProcessor::_updateEncLists(){
  //Remove first item from list
  _encTicksList.pop_front();
  //Append encoder ticks value to end of list
  _encTicksList.push_back(_encTicks);

  //Clear zeroedEncTicksList
  _zeroedEncTicksList = {};

  //Obtain value of first item in encTicksList
  double firstVal = _encTicksList.front();

  //Append data in encTicksList to zeroedEncTicksList while subtracting away value of first term
  for (auto const& iterator: _encTicksList){
    double value = iterator - firstVal;
    _zeroedEncTicksList.push_back(value);
  }
}*/


//Return orientation of motor shaft in degrees (//range of plus or minus 180)
double EncoderDataProcessor::degreesPosition(){
  double accumulatedDegrees = degreesAccumulated();
  //Converting angle to a (0,360] representation
  double angle360 = fmod(accumulatedDegrees,360.0);
  if(angle360 > 180){
    return angle360 - 360;
  }
  else if(angle360 <= -180){
    return angle360 + 360;
  }
  else{
    return angle360;
  }
}

double EncoderDataProcessor::adjustedDegreesPosition(){
	if(_wheel){
		double angle360 = fmod( _adjustedWheelDeg, 360.0);
  		if(angle360 > 180){
  		  return angle360 - 360;
  		}
  		else if(angle360 <= -180){
  		  return angle360 + 360;
  		}
  		else{
  		  return angle360;
  		}
	}
	else{
		return _adjustedEncTicks*360.0/_ticksPerRev;
		double angle360 = fmod( _adjustedEncTicks*360.0/_ticksPerRev, 360.0);
  		if(angle360 > 180){
  		  return angle360 - 360;
  		}
  		else if(angle360 <= -180){
  		  return angle360 + 360;
  		}
  		else{
  		  return angle360;
  		}
	}
}

double EncoderDataProcessor::adjustedRadianPosition(){
	return adjustedDegreesPosition()*PI/180;
}


double EncoderDataProcessor::LPF_speed(double newSpeed){
	double cutoff_time = 1/_cutoff_freq;
	double alpha = cutoff_time/(cutoff_time + _sampling_time);
	double filteredSpeed = alpha*_speed + (1.0 -alpha)*newSpeed;
	return filteredSpeed;
}

void EncoderDataProcessor::_updateSpeed(){
	double newSpeed;
	if (_wheel){
		newSpeed = fmod(_adjustedWheelDeg - _previousAdjWheelDeg,360.0)/_sampling_time;
		_previousAdjWheelDeg = _adjustedWheelDeg;
	}else{
		newSpeed = (_adjustedEncTicks - _previousAdjEncTicks)*360.0/(_ticksPerRev*_sampling_time);
		_previousAdjEncTicks = _adjustedEncTicks;
	}
	//_speed = LPF_speed(newSpeed);
	_speed = (newSpeed);//Returns speed in deg per second
}


//Return angular speed of motor
double EncoderDataProcessor::speed(){
  return _speed;
}

//Return total number of degrees through which the motor has rotated since startup or since reset() was called
double EncoderDataProcessor::degreesAccumulated(){
  double numberOfTicks = _encTicks;
  double numberOfDegrees = (numberOfTicks/_ticksPerRev)*360;
  return numberOfDegrees;
}


//Return orientation of motor shaft in degrees (range of plus or minus 180)
double EncoderDataProcessor::radianPosition(){
  double accumulatedDegrees = degreesAccumulated();
  //Converting angle to a (0,360] representation
  double angle360 = fmod(accumulatedDegrees,360.0);
  float angle2pi = angle360*PI/180.0;
  if(angle360 > PI){
    return angle360 - 2*PI;
  }
  else if(angle360 <= -PI){
    return angle360 + 2*PI;
  }
  else{
    return angle2pi;
  }
}
//Function which returns encoder ticks
long EncoderDataProcessor::ticks(){
  return _adjustedEncTicks;
}


//Function which returns estimate of angular acceleration
/*double EncoderDataProcessor::acceleration(){
  return _acceleration;
}*/

//Function which resets/re-initializes the encoder values at 0 - encoder instance must be reset as well
//void EncoderDataProcessor::reset(){
//  noInterrupts();
//  _encTicks = 0;
//  _adjustedEncTicks = 0;
//	_adjustedWheelDeg = 0;
//	if(_wheel){
//		_deadBandUpper = _playInDegrees/2.0;
//		_deadBandLower = -_playInDegrees/2.0;
//	}
//	else{
//		_deadBandUpper = (_playInDegrees/2.0)*_ticksPerRev/(360.0); //Deadband is defined in terms of ticks
//		_deadBandLower = -(_playInDegrees/2.0)*_ticksPerRev/(360.0);
//	}  
//  _speed = 0;
//  //_acceleration = 0;
//
//  for (unsigned int j = 0; j < _encTicksList.size(); j++){
//    _encTicksList.pop_front();
//    _encTicksList.push_back(0);
//    _zeroedEncTicksList.pop_front();
//    _zeroedEncTicksList.push_back(0);
//	_wheelDegList.pop_front();
//	_wheelDegList.push_back(0);
//	_zeroedWheelDegList.pop_front();
//	_zeroedWheelDegList.push_back(0);
//  }
//
//  _coeffs[0] = 0; _coeffs[1] = 0; _coeffs[2] = 0;
//
//  for (unsigned int j = 0; j < _previousSpeeds.size(); j++){
//    _previousSpeeds.pop_front();
//    _previousSpeeds.push_back(0);
//  }
//  interrupts();
//}
