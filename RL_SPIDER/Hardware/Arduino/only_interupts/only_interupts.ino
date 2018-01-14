#define ledPin 13

void setupTimer2() {
  noInterrupts();
  // Clear registers
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2 = 0;

  // 200.32051282051282 Hz (16000000/((77+1)*1024))
  OCR2A = 77;
  // CTC
  TCCR2A |= (1 << WGM21);
  // Prescaler 1024
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20);
  // Output Compare Match A Interrupt Enable
  TIMSK2 |= (1 << OCIE2A);
  interrupts();
}
volatile boolean value;
void setup() {
  pinMode(ledPin, OUTPUT);
  setupTimer2();
}

void loop() {
}

ISR(TIMER2_COMPA_vect) {
  digitalWrite(ledPin, value);
  value = !value;
}
