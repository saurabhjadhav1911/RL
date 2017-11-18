int pin = 2;
unsigned long val=0;
void setup() {
  // put your setup code here, to run once:
  pinMode(pin, INPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = pulseIn(pin, HIGH);
  Serial.println(1000000.0 / val);
}
