
// getMotorSpeed() updates the encoder struct (global), use ENCDX.Vel & ENCDX.Pos as needed
void getMotorData() {

  cli();  //disable interrupts
  double dT = (double)lastTime_ENCD / 1000000; //scale by 10^6 for [us] -> [s]
  lastTime_ENCD = 0; //[us]

  ENCD1.Vel = ((((double)cntEncd1 - (double)ENCD1.lastCnt) / dT) * Pos_Cnts2Rev) * vel_LPF + ENCD1.Vel * (1 - vel_LPF); // [rev/s]
  ENCD2.Vel = ((((double)cntEncd2 - (double)ENCD2.lastCnt) / dT) * Vel_Cnts2Rev) * vel_LPF + ENCD2.Vel * (1 - vel_LPF);
  ENCD3.Vel = ((((double)cntEncd3 - (double)ENCD3.lastCnt) / dT) * Pos_Cnts2Rev) * vel_LPF + ENCD3.Vel * (1 - vel_LPF);
  ENCD4.Vel = ((((double)cntEncd4 - (double)ENCD4.lastCnt) / dT) * Vel_Cnts2Rev) * vel_LPF + ENCD4.Vel * (1 - vel_LPF);

  //save current position for next time
  ENCD1.lastCnt = (double)cntEncd1;   ENCD2.lastCnt = (double)cntEncd2;
  ENCD3.lastCnt = (double)cntEncd3;   ENCD4.lastCnt = (double)cntEncd4;

  ENCD1.Pos = (double)((int)cntEncd1 % Pos_CntsPerRev) * Pos_Cnts2Rev * 2 * Pi; // [rad]
  ENCD2.Pos = (double)((int)cntEncd2 % Vel_CntsPerRev) * Vel_Cnts2Rev * 2 * Pi;
  ENCD3.Pos = (double)((int)cntEncd3 % Pos_CntsPerRev) * Pos_Cnts2Rev * 2 * Pi;
  ENCD4.Pos = (double)((int)cntEncd4 % Vel_CntsPerRev) * Vel_Cnts2Rev * 2 * Pi;

  sei(); //enable interrupts

}
