#include <Servo.h>
#define number_of_states 2

Servo myservo1, myservo2; // create servo object to control a servo

String data;
static volatile int av[number_of_states], pav, state = 0 , val[number_of_states] = {0, 0}, mn = 1024, mx = 0, angle, lv[number_of_states], sense_pin = 13;
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
      myservo1.write(val[0]);
      myservo2.write(val[1]);
      flag = false;
    }
    if (sendflag) {
      for (int s = 0; s < number_of_states; s++) {
        av[s] = (analogRead(s) + lv[s]) / 2;
      }

      for (int s = 0; s < number_of_states; s++) {
        Serial.print(val[s]);
        Serial.print(' ');
        Serial.print(av[s]);
        Serial.print(' ');
      }

      Serial.print('|');

    }
    filterflag = !filterflag;
  }
  else {
    for (int s = 0; s < number_of_states; s++) {
      lv[s] = analogRead(s);
    }
    filterflag = !filterflag;
  }
}

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
  Serial.begin(115200);
  setupTimer2();
  myservo1.attach(6);
  myservo2.attach(10);
  pinMode(sense_pin, OUTPUT);

}
char c;
void loop() {
  if (Serial.available())
  {
    sendflag = false;
    c = Serial.read();
    switch (c)
    {
      case (' '):
        {
          val[state] = constrain(data.toInt(), 0, 180);
          data = "";
          state++;
          break;
        }
      case ('|'):
        {
          val[state] = constrain(data.toInt(), 0, 180);
          data = "";
          flag = true;
          sendflag = true;
          state = 0;
          break;
        }
      default: {
          data += c;
        }
    }
  }
}

