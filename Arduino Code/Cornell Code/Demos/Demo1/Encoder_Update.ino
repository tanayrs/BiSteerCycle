
// getMotorSpeed() updates the encoder struct (global), use ENCDX.Vel as needed
void getMotorSpeed() {

  cli();  //disable interrupts
  double dT = (double)lastTime_ENCD / 1000000; //scale by 10^6 for [us] -> [s]
  lastTime_ENCD = 0; //[us]

  ENCD1.Vel = (((double)cntEncd1 - (double)ENCD1.lastCnt) / dT) * Cnts2Rev; // [rev/s]
  ENCD2.Vel = (((double)cntEncd2 - (double)ENCD2.lastCnt) / dT) * Cnts2Rev;

  //save current position for next time
  ENCD1.lastCnt = (double)cntEncd1;
  ENCD2.lastCnt = (double)cntEncd2;

  ENCD1.Pos = (double)((int)cntEncd1 % CntsPerRev) * Cnts2Rev * 2 * Pi; // [rad]
  ENCD2.Pos = (double)((int)cntEncd2 % CntsPerRev) * Cnts2Rev * 2 * Pi;

  sei(); //enable interrupts
  
}
