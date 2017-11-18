#include <Servo.h>


Servo myservo;  // create servo object to control a servo

String data;
static volatile int av, pav, val = 0, mn = 1024, mx = 0, angle, lv, sense_pin = 13;
static volatile boolean flag = false, sendflag = true, filterflag = false, sense_val = true;
long last_time = 0, interval = 1000;

ISR(TIMER2_COMPA_vect)
{
  //motor(255, 255);
  /*Serial.println("gfghf");*/
  sense_val = !sense_val;
  digitalWrite(sense_pin, sense_val);
}
void setup() {
  // TIMER 2 for interrupt frequency 1000 Hz:
  // TIMER 2 for interrupt frequency 2000 Hz:
  cli(); // stop interrupts
  TCCR2A = 0; // set entire TCCR2A register to 0
  TCCR2B = 0; // same for TCCR2B
  TCNT2  = 0; // initialize counter value to 0
  // set compare match register for 2000 Hz increments
  OCR2A = 249; // = 16000000 / (32 * 2000) - 1 (must be <256)
  // turn on CTC mode
  TCCR2B |= (1 << WGM21);
  // Set CS22, CS21 and CS20 bits for 32 prescaler
  TCCR2B |= (0 << CS22) | (1 << CS21) | (1 << CS20);
  // enable timer compare interrupt
  TIMSK2 |= (1 << OCIE2A);
  sei(); // allow interrupts
  sei(); // allow interrupts
  pinMode(sense_pin, OUTPUT);

}

void loop() {

}
