// see 'Encoder Method' for info on what this is

// Encoder 1
void ENCD1_ISR() {
  static uint8_t enc_val = 0;
  enc_val = (enc_val << 2) | ((GPIOC_PDIR >> 1) & 0b0011);
  cntEncd1 += ENCODER_LOOKUP[enc_val & 0b1111];
}

// Encoder 2
void ENCD2_ISR() {
  static uint8_t enc_val = 0;
  enc_val = (enc_val << 2) | ((GPIOC_PDIR >> 6) & 0b0011);
  cntEncd2 += ENCODER_LOOKUP[enc_val & 0b1111];
}

// Encoder 3
void ENCD3_ISR() {
  static uint8_t enc_val = 0;
  enc_val = (enc_val << 2) | ((GPIOB_PDIR) & 0b0011);
  cntEncd3 += ENCODER_LOOKUP[enc_val & 0b1111];
}

// Encoder 4
void ENCD4_ISR() {
  static uint8_t enc_val = 0;
  enc_val = (enc_val << 2) | ((GPIOB_PDIR >> 2) & 0b0011);
  cntEncd4 += ENCODER_LOOKUP[enc_val & 0b1111];
}
