#define threshold 512
#define r1 4
#define r2 5
#define sr 6
#define l1 8
#define l2 7
#define sl 9
#define lspd 230
#define rspd 255
#define dis 3.0
#define Kp 50.0
#define Ki 0.0
#define Kd 0.0
#define condist 10
int c, sensorvalues[6];
float pinput, input, output, P, I, D;
boolean s[5];
void motor(int lsp, int rsp)
{
  Serial.print(lsp + "  " + rsp);
  if (lsp >= 0) {
    /*
      digitalWrite(l1, 1);
      digitalWrite(l2, 0);*/

    PORTB |= 0b00000001;
    PORTD &= 0b01111111;
    analogWrite(sl, lsp);
  }
  else {
    /*
      digitalWrite(l1, 0);
      digitalWrite(l2, 1);*/
    PORTD |= 0b10000000;
    PORTB &= 0b11111110;
    analogWrite(sl, -lsp);
  }

  if (rsp >= 0) {
    /*
      digitalWrite(r1, 1);
      digitalWrite(r2, 0);*/

    PORTD |= 0b00010000;
    PORTD &= 0b11011111;
    analogWrite(sr, rsp);
  }
  else {
    //digitalWrite(r1, 0);
    //digitalWrite(r2, 1);
    PORTD |= 0b00100000;
    PORTD &= 0b11101111;
    analogWrite(sr, -rsp);
  }
}
int sense()
{
  for (int i = 0; i < 3; i++)
  { s[i] = 0;
  }
  c = 0;
  if (analogRead(A0) > threshold)
  { s[0] = 1;
    c = c + 0b1;
  }
  if (analogRead(A2) > threshold)
  { s[1] = 1;
    c = c + 0b10;
  }
  if (analogRead(A3) > threshold)
  { s[2] = 1;
    c = c + 0b100;
  }
  if (analogRead(A4) > threshold)
  { s[3] = 1;
    c = c + 0b1000;
  }
  if (analogRead(A5) > threshold)
  { s[4] = 1;
    c = c + 0b10000;
  }
  return c;
}
void gen()
{
  if (c)
  {
    input = ((float)(((sensorvalues[0] - 65)) + (2 * (sensorvalues[1] - 65)) + (3 * (sensorvalues[2] - 65)) + (4 * (sensorvalues[3] - 65)) + (5 * (sensorvalues[4] - 65))) / (sensorvalues[0] + sensorvalues[1] + sensorvalues[2] + sensorvalues[3] + sensorvalues[4] - 325));

    P = Kp * input;
    D = Kd * (input - pinput);
    I += Ki * input;
    output = P + I + D;
    pinput = input;
    Serial.println(output);
    if (output >= 0)
    {
      motor(lspd, (rspd - output));
    }
    else
    {
      motor((lspd + output), rspd);
    }
  }
}
/*
  void sense()
  {
  sensorvalues[0] = analogRead(A0);
  sensorvalues[1] = analogRead(A2);
  sensorvalues[2] = analogRead(A3);
  sensorvalues[3] = analogRead(A4);
  sensorvalues[4] = analogRead(A5);
  c = (16 * (sensorvalues[0] / threshold) + 8 * (sensorvalues[1] / threshold) + 4 * (sensorvalues[2] / threshold) + 2 * (sensorvalues[3] / threshold) + (sensorvalues[4] / threshold));

  }*/

void setup() {
  cli();
  pinMode(12, INPUT_PULLUP);
  pinMode(l1, 1);
  pinMode(l2, 1);
  pinMode(sl, 1);
  pinMode(r1, 1);
  pinMode(r2, 1);
  pinMode(sr, 1);
  Serial.begin(115200);
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
void loop() {
  getParam();
}
ISR(TIMER0_COMPA_vect)
{
  //motor(255, 255);
  /*Serial.println("gfghf");*/
  sense();
  gen();
}
