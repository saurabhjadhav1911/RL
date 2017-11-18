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
  if (filterflag)
  {
    if (flag)
    {
      myservo.write(val);
      flag = false;
    }
    if (sendflag) {
      av = (analogRead(A0) + lv) / 2;
      Serial.print(av);
      Serial.print('|');
    }
    filterflag = !filterflag;
  }
  else {
    lv = analogRead(A0);
    filterflag = !filterflag;
  }
}
void setup() {
  Serial.begin(115200);
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
  myservo.attach(9);
  pinMode(sense_pin, OUTPUT);

}
char c;
void loop() {
  if (Serial.available())
  {
    sendflag = false;
    c = Serial.read();

    if (c == '|') {
      val = data.toInt();
      val = constrain(val, 0, 180);
      data = "";
      flag = true;
      sendflag = true;
    }
    else {
      data += c;
    }
  }
  /*
    if (Serial.available())
    {
      c = Serial.read();
      if (c == '|')
      {
        val = data.toInt();
        val = constrain(val, 0, 180);
        data = "";
      }
      else
      {
        data += c;
      }
    }
  */
}

