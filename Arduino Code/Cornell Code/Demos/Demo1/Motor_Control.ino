
void setMotor(uint8_t Pins[3], double mySpeed) {
  if (mySpeed >= 0) { //Forward
    digitalWrite(Pins[0], HIGH);
    digitalWrite(Pins[1], LOW);
    analogWrite(Pins[2], (uint8_t)mySpeed);
  }
  else {  //Reverse
    digitalWrite(Pins[1], HIGH);
    digitalWrite(Pins[0], LOW);
    analogWrite(Pins[2], (uint8_t) - mySpeed);
  }
}

void brakeMotor(uint8_t Pins[3], uint8_t mySpeed) {
  digitalWrite(Pins[0], LOW);
  digitalWrite(Pins[1], LOW);
}
