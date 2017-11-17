
// Arduino Code for the Motor Speed Control Lab

// Likely User Modified Variables ******************************
unsigned long deltaT = 20000; // time between samples (usecs) 1000->50000


// End Likely User Modified Variables***************************

// For arduino and host interface, NO NEED TO MODIFY!
unsigned long transferDt = 20000; // usecs between host updates
int angleSensorPin = A0;
int pwmVoltagePin = A1;
int motorVoltagePin = A2;
int motorOutputPin = 9;  // Do not change this!!

// Arduino-specific DAC values.
int dacMax = 255; // Arduino dac is eight bits.
int adcMax = 1024;  //Arduino uses a 10 bit dac, 10th power of 2 = 1024
int adcCenter = 512; // 1024/2 = 512


bool first_time = true;
String config_message_7_bytes = "&A~Desired~5&C&S~K_P~P~0~10~0.05&S~Direct~O~0~260~0.01&S~Desired~A~0~260~1&T~MotorSpeed~U1~0~260&T~ArmAngle~S1~-150~150&T~MotorCmd~U1~0~260&H~2&";
String config_message = config_message_7_bytes; //for 7 bytes set the print

// Control variables (set by host).
int direct; // Direct motor command from host.
float desired;  // Desired value (speed or angle) from host.
float Kp; // Feedback gains (proportional)

// Variables to reset every time loop restarts.
int loop_counter;
int numSkip;  // Number of loops to skip between host updates.
String inputString = ""; //holds received serial data.
boolean stringComplete; // String received flag.


// Setup sets up pwm frequency (30khz), initializes past values.
int loopPin = 13;
boolean loopFlag;

void setup() {
  // Set up inputs
  pinMode(motorVoltagePin, INPUT);
  pinMode(pwmVoltagePin, INPUT);
  pinMode(angleSensorPin, INPUT);
  
  // Set up PWM motor output pin, affects delay() function
  // Delay argument will be in 1/64 milliseconds.
  pinMode(motorOutputPin,OUTPUT);
  digitalWrite(motorOutputPin,LOW);
  setPwmFrequency(motorOutputPin, 1); // Set pwm to approx 30khz.

  // Set for fastest serial transfer.
  Serial.begin(115200);

  // Initialization for data transfer from host.
  inputString.reserve(10);  // Reserve space for rcvd data   
  stringComplete = false;
  numSkip = max(int((transferDt+100)/deltaT),1);  // Number of loops between host transfers.
  loop_counter = 0;  // Initialize counter for status transfer

  // Initialize inputs from host.
  initInputs();

  // Initialize timeSync
  timeSyncInit();

  // Diagnostic
  pinMode(loopPin,OUTPUT);
  loopFlag = false;

}


// Main code, runs repeatedly
void loop() {
  
  // Check if first time.
  startup();
  
  // Make sure loop start is deltaT microsecs since last start
  int headroom = timeSync(deltaT);
  
  // Invert monitor 
  //digitalWrite(loopPin,loopFlag);
  //loopFlag = !loopFlag;
  
  // User modifiable code between stars!!
  /***********************************************/
  // Measure the voltage across the motor and the voltage at the drive transistor.
  // Read each voltage three times and sum, and divide later. This averaging reduces noise.
  int VmotorADC = analogRead(motorVoltagePin);
  int VpwmADC = analogRead(pwmVoltagePin);
  int VangleADC = analogRead(angleSensorPin) - adcCenter;

  // Compute the measured backEMF, which is proportional to motor speed, by
  // offsetting the motor voltage with the voltage across the 1/2 ohm resistor.
  // Convert to an integer between 0 -> 256 by dividing by six.
  float motorSpd = 0.5*float(VmotorADC - (VpwmADC - VmotorADC));
  float armAngle = 0.25*float(VangleADC); 
  
  // Compute the error, which is the difference between desired and measured speed.
  float error = desired - motorSpd;
  
  // Compute and limit the motor output command.
  int motorCmd = int(Kp * error + direct);
  motorCmd = min(max(motorCmd, 0), dacMax);
  analogWrite(motorOutputPin,motorCmd);
  
  /***********************************************/
  
  //check for new parameter values!
  serialEvent();  
  if(stringComplete) processString();
  
  // Transfer to host occasionally
  if (loop_counter % numSkip == 0) {
    loop_counter = 0;
    printStatus(int(motorSpd), int(armAngle), motorCmd, headroom);
  }

  // Increment the loop counter.
  loop_counter++;

}

// YOU SHOULD NOT NEED TO MODIFY ANY CODE BELOW THIS LINE!!!!!!!!!
// Creates a signed byte number from val, without using 0 and 255
byte signedByte(int val) {
  return byte(min(max(val+128,1),254));
}

char buf[8];  // five bytes to hold data for host.
// Packs up a 5-byte status package for host.
void printStatus(int mSpd, int error, int mCmd, int hdrm) {
  char *d;
  d = buf;
  // Start Byte.
  *d = byte(0);
  d++;
  *d = (uint8_t) min(max(mSpd,0),255);
  d++;
  *d = (int8_t) min(max(error,-128),127);
  d++;
  *d = (uint8_t) min(max(mCmd,0),255);
  d++;
  memcpy(d,&hdrm,2);
  d+=2;
  // Stop byte (255 is not unique).
  *d = byte(255);

  // Write the buffer to the host.
  Serial.write(buf, 7);//for 7 byte message.
}

void initInputs() {
  // Initial values for variables set from host.
  desired = 0;
  Kp = 0;
  direct = 0;//direct term in motor command
}

void serialEvent() {
  if (! first_time){
    while (Serial.available()) {
      // get the new byte:
      char inChar = (char)Serial.read();
      // add it to the inputString:
      inputString += inChar;
      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == '\n') {
        stringComplete = true;
        break;
      }
    }
  }
}



void processString() {
char St = inputString.charAt(0);
  inputString.remove(0,1);
  float val = inputString.toFloat();
  switch (St) {
    case 'P': 
      Kp = val;
      break;
    case 'O':  
      direct = val;
      break;
    case 'A':  
      desired = val;
      break;
    case '~':
      first_time = true;
      break;
    default:
    break;  
  }
  inputString = "";
  stringComplete = false;
}


void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
        TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}

unsigned long starttime;
unsigned long headroom_ts;
boolean switchFlag;
unsigned long scaleT = 1;
int monitorPin = 8;  // for checking time sync

void timeSyncInit() {
  // Frequency Monitor
  pinMode(monitorPin, OUTPUT);
  digitalWrite(monitorPin,LOW);
  if (motorOutputPin == 5 || motorOutputPin == 6) {
    scaleT = 64;
  } else {
    scaleT = 1;
  }
  headroom_ts = deltaT;
  starttime = micros();
  switchFlag = true;
}


// Wait until it has been deltaT since this was last called.
// Returns headroom, delay in units of 5us.
int timeSync(unsigned long dT) {
 
  unsigned long delayMuS = max((dT - (micros()-starttime))/scaleT, 1);
  if (delayMuS > 5000) {
    delay(delayMuS / 1000); 
    delayMicroseconds(delayMuS % 1000);
  } else {
    delayMicroseconds(delayMuS); // Wait to start exactly deltaT after last start
  }

  headroom_ts = min(headroom_ts,delayMuS);  // min loop headroom should be > 0!!
  starttime = micros(); // Note time loop begins
    
  // Output square wave on monitor pin
  digitalWrite(monitorPin, switchFlag);
  switchFlag = !switchFlag;

  return min(headroom_ts, 32767); // Truncate headroom_ts to an int.
}

bool init_gui(){
  delay(1);
  if(Serial.available()){
    while (Serial.available()) {
      // get the new byte:
      char inChar = (char)Serial.read();
      // add it to the inputString:
      inputString += inChar;
      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == '\n') {
        stringComplete = true;
        break;
      }
    }
    if (inputString=="SET\n"){
      first_time = false;
      return true;//gui initialized
    }
  }
  return false;
}

void startup(){
    if (first_time){
    Serial.println(config_message);
    while (first_time){  //wait here until complete/happy
      bool is_ok = init_gui();
      if (is_ok){
        delay(2000);
        timeSyncInit(); //right before loop proper starts
      }
    }
  }
}

