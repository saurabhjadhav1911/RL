#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int av, pav;

ISR(TIMER0_COMPA_vect)
{
  //motor(255, 255);
  /*Serial.println("gfghf");*/
  av = analogRead(A0);
  mx = max(mx, av);
  mn = min(mn, av);
  angle = ((av - mn) * 180.0) / (mx - mn);

  Serial.println(angle);
}

void setup() {
  Serial.begin(115200);
  myservo.attach(9);
  // TIMER 0 for interrupt frequency 1000 Hz:
  cli(); // stop interrupts
  TCCR0A = 0; // set entire TCCR0A register to 0
  TCCR0B = 0; // same for TCCR0B
  TCNT0  = 0; // initialize counter value to 0
  // set compare match register for 1000 Hz increments
  OCR0A = 249; // = 16000000 / (64 * 1000) - 1 (must be <256)
  // turn on CTC mode
  TCCR0B |= (1 << WGM01);
  // Set CS02, CS01 and CS00 bits for 64 prescaler
  TCCR0B |= (0 << CS02) | (1 << CS01) | (1 << CS00);
  // enable timer compare interrupt
  TIMSK0 |= (1 << OCIE0A);
  sei(); // allow interrupts


}
String data;
int val, mn = 1024, mx = 0, angle;
long last_time = 0, interval = 2000;
void loop() {
  if (Serial.available())
  {
    data = Serial.readStringUntil('|');
    val = data.toInt();

    val = constrain(val, 0, 180);
    myservo.write(val);
  }


  /*
    Serial.print(' ');
    Serial.println(val);
  */

}

