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
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2 = 0;

  // 100.16025641025641 Hz (16000000/((155+1)*1024))
  
  OCR2A = 155;
  // CTC
  TCCR2A |= (1 << WGM21);
  // Prescaler 1024
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20);
  // Output Compare Match A Interrupt Enable
  TIMSK2 |= (1 << OCIE2A);
  sei(); // allow interrupts
  
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

