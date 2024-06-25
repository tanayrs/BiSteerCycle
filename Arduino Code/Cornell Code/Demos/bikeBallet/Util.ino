//calculates the control inputs from the PID controllers and actuates the motors
void setMotors_PID() {
  
  double uM1 = vel1_Cmd + sign(vel1_Ref) * sq(vel1_Ref * MOTOR1_FF) - vel2_Ref * MOTOR1_WHEEL_REF_FF;
  double uM2 = vel2_Cmd + vel2_Ref * MOTOR2_FF;
  double uM3 = vel3_Cmd + sign(vel3_Ref) * sq(vel3_Ref * MOTOR3_FF) - vel4_Ref * MOTOR3_WHEEL_REF_FF;
  double uM4 = vel4_Cmd + vel4_Ref * MOTOR4_FF;

  setMotor(MOTOR1, uM1);
  setMotor(MOTOR2, uM2);
  setMotor(MOTOR3, uM3);
  setMotor(MOTOR4, uM4);
  
}

//set 1 motor to a certain speed, include deadband
void setMotor(const uint8_t Pins[4], double mySpeed) {
  if (mySpeed >= 0) { //Forward
    digitalWrite(Pins[0], HIGH);
    digitalWrite(Pins[1], LOW);
    analogWrite(Pins[2], (uint8_t)mySpeed + Pins[3]);
  }
  else {  //Reverse
    digitalWrite(Pins[1], HIGH);
    digitalWrite(Pins[0], LOW);
    analogWrite(Pins[2], (uint8_t) - mySpeed + Pins[3]);
  }
}

//brake 1 motor, just incase the deadband is too high
void brakeMotor(const uint8_t Pins[4]) {
  digitalWrite(Pins[0], LOW);
  digitalWrite(Pins[1], LOW);
  analogWrite(Pins[2], 0;
}

double sign(double myX) {
  return (myX > 0) - (myX < 0);
}
