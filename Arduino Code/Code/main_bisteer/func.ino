/****************** Functions ******************/

/* Setting Encoder Pins to PULLUP and Initialises Ticks */
void startup_routine() {
        analogWriteResolution(12);
        init_bno();

        // Reference: void EncoderDataProcessor::update(long ticks,double steerAccumulatedTicks,double steerTicksOffset) //
        frontSteerData.update(0, 0, 0);
        rearSteerData.update(0, 0, 0);
        frontWheelData.update(0, 0, 0);
        rearWheelData.update(0, 0, 0);

        // Setting Encoder Pins to PULLUP //
        pinMode(rearWheelEnc1, INPUT_PULLUP);
        pinMode(rearWheelEnc2, INPUT_PULLUP);
        pinMode(rearSteerEnc1, INPUT_PULLUP);
        pinMode(rearSteerEnc2, INPUT_PULLUP);

        pinMode(frontWheelEnc1, INPUT_PULLUP);
        pinMode(frontWheelEnc2, INPUT_PULLUP);
        pinMode(frontSteerEnc1, INPUT_PULLUP);
        pinMode(frontSteerEnc2, INPUT_PULLUP);

        frontWheelInput = 0;
        rearWheelInput = 0;
        
        frontSteerInput = 0;
        rearSteerInput = 0;
        
        loopTimeMicros = 0;
        runTimeMillis = 0;

        int_track = 0;
}

/* Sets Steering Angle for Front and Rear Wheels */
float* PWPF(float controlSignal, float Uon, float Uoff, float prev_output) {
        static float result[2];
        float PWPF_output = prev_output;
          
        if (controlSignal > Uon) {
                PWPF_output = 1;
        } else if (controlSignal < -Uon) {
                PWPF_output = -1;
        } else if (prev_output > 0) {
                if (controlSignal < Uoff) {
                        PWPF_output = 0;
                } else {
                        PWPF_output = prev_output;
                }
        } else if (prev_output < 0) {
                if (controlSignal > -Uoff) {
                        PWPF_output = 0;
                } else {
                        PWPF_output = prev_output;
                }
        } else {
                PWPF_output = prev_output;
        }
        
        // Update the previous output state
        prev_output = PWPF_output;

        result[0] = PWPF_output;
        result[1] = prev_output; 
        
        return result;
}

/* Returns Sign of val: -1 or 1 */
int sgn(double val){
        return val>0?1:-1;
}