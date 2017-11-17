//Likely User Modified Variables ******************************

unsigned int deltaT = 1000;         // Sample period in microseconds.
int angleAverages = 5;
int past_size = 3;                 // interval for delta, larger=less noise, more delay.
unsigned long transferDt = 20000; // usecs between host updates  
float Kp, Kd, Kbemf, Ku, Ki, directV, desiredV;
                                 
// ***************************************************************

// Teensy definitions
#define angleSensorPin  A9
#define pwmVoltagePin A0
#define motorVoltagePin  A1
#define motorOutPWM  3
#define monitorPin 2  
#define dacRes 12   // Teensy 12-bit dac resolution, max val 4095
#define dacMax 4095
#define adcRes 14
#define adcCenter 8192 //Teensy ADC set to 14 bits, 16384/2 = 8192
#define adcMax 16383

// Circuit Specific Definitions.
#define scaleVadc 5.0 // All signals 0->5 volts.
#define vDrive 5.0 // Driver peak voltage.
#define rShunt 0.5 // Resistor from motor to ground.
#define rMotor 0.5 // Motor series resistance.

// Variables for Conversion
#define deg2rad 0.0175    
#define twopi 6.2831853  

//Rest of Setup:
bool first_time;
String config_message_30_bytes = "&A~DesiredAngV~5&C&S~Direct~O~0~5.0~0.1&S~DesiredAngV~A~-1~1~0.1&T~AngleV~F4~-2.5~2.5&T~BackEMF~F4~0~5&T~MCmd~F4~0~5&H~4&";
String config_message = config_message_30_bytes;

float rad2deg = 1.0/deg2rad;        // 180/pi
 
float dTsec = 1.0e-6*deltaT;       // The period in seconds. 
float scaleD = 1.0/(dTsec*past_size); // Divide deltas by interval.    
                             
float errorVintegral;                // Variable for integrating angle errors.
float integralMax = 200;            // Maximum value of the integral

int loopCounter;

// Storage for past values.
float pastErrorV[20];  // Should be larger array than past_size.
char buf[60];  // 

// Variables for loop control
uint32_t loop_counter;
int numSkip;  // Number of loops to skip between host updates.
elapsedMicros loopTime; // Create elapsed time variable to ensure regular loops.
unsigned int headroom;  // Headroom is time left before loop takes too long.
boolean switchFlag;

// Initializes past values.
void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  // Set up inputs
  analogReadResolution(adcRes);
  pinMode(motorVoltagePin, INPUT);
  pinMode(pwmVoltagePin, INPUT);
  pinMode(angleSensorPin, INPUT);

  // Set up output
  analogWriteResolution(dacRes);
  pinMode(motorOutPWM, OUTPUT);
  analogWriteFrequency(motorOutPWM, 23437.5); // Teensy 3.0 pin 3 also changes to 23437.5 kHz
  analogWrite(motorOutPWM, LOW);
  
  // Frequency Monitor
  pinMode(monitorPin, OUTPUT);

  // Number of loops between transfers to host.
  numSkip = max(int((transferDt+100)/deltaT),1); 

  first_time = false;

}

void loop() {  // Main code, runs repeatedly
  
  // Reinitializes or updates from sliders on GUI.
  startup();
  
  // Make sure loop starts deltaT microsecs since last start
  unsigned int newHeadroom = max(int(deltaT) - int(loopTime), 0);
  headroom = min(headroom, newHeadroom);
  
  while (int(loopTime) < int(deltaT)) {};
  loopTime = 0;
  
  // Monitor Output should be a square wave with frequency = 1/(2*deltaT) 
  switchFlag = !switchFlag;
  digitalWrite(monitorPin, switchFlag);

 
  /*************** Section of Likely User modifications.**********************/
  // Read Angle, average to reduce noise.
  int angleI = 0;
  for(int i = 0; i < angleAverages; i++) angleI += analogRead(angleSensorPin);
  float angleV = scaleVadc*float(angleI- angleAverages*adcCenter)/float(angleAverages*adcMax);
  
  // Read motor voltage and pmw voltage
  float motorV = scaleVadc*float(analogRead(motorVoltagePin))/float(adcMax);
  float pwmV = scaleVadc*float(analogRead(pwmVoltagePin))/float(adcMax);
  float motor_current = (pwmV - motorV)/rShunt;
  float motor_bemf = motorV - rMotor*motor_current;  // Ignores L(di/dt).

  // Compute and write out motor command.
  float motorCmd = directV;
  float motorCmdLim = min(max(motorCmd, 0), vDrive);
  analogWrite(motorOutPWM,int((motorCmdLim/vDrive)*dacMax));

  if (loopCounter == numSkip) {  // Lines below are for debugging.
    packStatus(buf, angleV, motor_bemf, motorCmdLim, float(headroom));
    Serial.write(buf,18);
    loopCounter = 0;
  } else loopCounter += 1;

}

void init_loop() {
  // Initialize loop variables
  loopCounter = 0; 
  headroom = deltaT;

  // Zero past errors
  for (int i = past_size-1; i >= 0; i--) pastErrorV[i] = 0;
}


// Initializes the loop if this is the first time, or if reconnect sent
// from GUI.  Otherwise, just look for serial event.
void startup(){
  if (first_time) {
    while(Serial.available() > 0) Serial.read(); // Clear out rcvr.
    Serial.println(config_message);  // Send the configuration files.
    while (! Serial.available()) {}  // Wait for serial return.
    while(Serial.available() > 0) {   // Clear out rcvr.
        Serial.read();
        //char inChar = (char) Serial.read(); 
        //if (inChar == '\n') break;
    }
    init_loop();
    first_time = false;
  } else {
    serialEvent();
  }
}


// Simple serial event, only looks for disconnect character, resets loop if found.
void serialEvent() {
  String inputString = ""; 
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    // if the incoming character is a newline, ready to process.
    if (inChar == '\n') {
      processString(inputString);
      inputString = "";
      break;
    }
  }
}

void processString(String inputString) {
char St = inputString.charAt(0);
  inputString.remove(0,1);
  float val = inputString.toFloat();
  switch (St) {
    case 'P': 
      Kp = val;
      break;
    case 'D':
      Kd = val;
      break;  
    case 'E':
      Kbemf = val;
      break;
    case 'U':
      Ku = val;
      break;
    case 'I':
      Ki = val;
      break;  
    case 'O':  
      directV = val;
      break;
    case 'A':
      desiredV = val;
      break;
    case '~':
      first_time = true;
      break;
    default:
    break;  
  }
}

// Load the serial output buffer.
void packStatus(char *buf, float a, float b, float c, float d) { // float e, float f, float g) {
  
  // Start Byte.
  buf[0] = byte(0);
  int n = 1; 
  
  memcpy(&buf[n],&a,sizeof(a));
  n+=sizeof(a);
  memcpy(&buf[n],&b,sizeof(b));
  n+=sizeof(b);
  memcpy(&buf[n],&c,sizeof(c));
  n+=sizeof(c);
  memcpy(&buf[n],&d,sizeof(d));
  n+=sizeof(d);
  /*
  memcpy(&buf[n],&e,sizeof(e));
  n+=sizeof(e);
  memcpy(&buf[n],&f,sizeof(f));
  n+=sizeof(f);
  memcpy(&buf[n],&g,sizeof(g));
  n+=sizeof(g);
*/
  // Stop byte (255 otherwise unused).
  buf[n] = byte(255); 
}

