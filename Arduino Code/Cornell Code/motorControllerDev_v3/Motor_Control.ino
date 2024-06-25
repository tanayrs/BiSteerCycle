
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

void brakeMotor(const uint8_t Pins[4], uint8_t mySpeed) {
  digitalWrite(Pins[0], LOW);
  digitalWrite(Pins[1], LOW);
}
