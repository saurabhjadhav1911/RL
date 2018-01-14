#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int val = 0;  // variable to read the value from the analog pin

void setup() {
  Serial.begin(115200);
  myservo.attach(9);
}
String data;
void loop() {

  myservo.write(val);
  delay(2000);
  val = 180 - val;
}

