/* Sets Motor Direction and analogWrite's Speed */
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

/* Stops Motor */
void brakeMotor(uint8_t Pins[3], uint8_t mySpeed) {
        digitalWrite(Pins[0], LOW);
        digitalWrite(Pins[1], LOW);
}

/* Some Statespace Feedback, need to know what myMu, vGlonal and epsilon is */
void feedbackLin(double vGlobal[2], double vBody[2]) {
        vBody[0] = vGlobal[0]*cos(myMu[2]) + vGlobal[1]*sin(myMu[2]);
        vBody[1] = (vGlobal[1]*cos(myMu[2]) - vGlobal[0]*sin(myMu[2]))/epsilon;
}
