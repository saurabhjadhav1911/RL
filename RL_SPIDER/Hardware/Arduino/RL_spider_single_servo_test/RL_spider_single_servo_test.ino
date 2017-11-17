#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

void setup() {
  cli();
  Serial.begin(115200);
  myservo.attach(9);
  TCCR0A = (1 << COM0A1) | (1 << WGM01);
  TCCR0B = (1 << CS00) | (1 << CS02);
  TIMSK0 = (1 << OCIE0A);
  OCR0A = 156;
  delay(1500);
  while (digitalRead(12) == 1)
  {}
  delay(1500);
  sei();
}
String data;
void loop() {
}
ISR(TIMER0_COMPA_vect)
{
  Serial.println(analogRead(A0));
  if (Serial.available())
  {
    data = Serial.readString();
    val = data.toInt();

    myservo.write(val);
  }
}

