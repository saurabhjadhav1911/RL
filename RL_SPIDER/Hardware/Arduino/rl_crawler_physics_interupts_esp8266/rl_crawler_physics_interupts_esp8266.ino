#include <ESP8266WiFi.h>
#define number_of_states 2

#define l1 150.0
#define l2 150.0
/*
WiFi.disconnect();
WiFi.mode(WIFI_OFF);
WiFi.forceSleepBegin();
delay(1);*/
// 
// ESP8266 Timer Example
// SwitchDoc Labs  October 2015
// 
extern "C"
{
  #include "user_interface.h"
}

String data;
static volatile int mn = 1024, mx = 0, angle, lv, sense_pin = 13, state = 0, p = 0, last_p = 0;
static volatile float K = 0.1, av[number_of_states], pav, val[number_of_states] =
{
  0, 0
};

static volatile double saved_x, saved_dx, saved_y, saved_dy, dx, dy, x, y;
static volatile boolean flag = false, sendflag = true, filterflag = false, sense_val = true;
char c;
os_timer_t myTimer;
bool tickOccured;
// start of timerCallback
void timerCallback(void * pArg)
{
  if (sendflag)
  {
    for (int s = 0; s < number_of_states; s++)
    {
      av[s] += (K * (val[s] - av[s]));
      Serial.print((int) val[s]);
      Serial.print(' ');
      Serial.print((int) av[s]);
      Serial.print(' ');
    }
    kinematics(av[0]*3.14159/180, av[1]*3.14159/180);
    Serial.print((int) p);
    Serial.print(' ');
    Serial.print((int) x);
    Serial.print(' ');
    Serial.print('|');
  }
}

// End of timerCallback
void kinematics(float theta1, float theta2)
{
  dx = ((l1 * sin(theta1)) + (l2 * sin(theta1 + theta2)));
  dy = ((l1 * cos(theta1)) + (l2 * cos(theta1 + theta2)));
  if (dy > 0)
    p = 0;
  else
    p = 1;
  if (p == 1 && last_p == 0)
  {
    // rising edge p
    saved_x = x;
    saved_dx = dx;
    // saved_y = y;
    // saved_dy = dy;
  }
  if (p == 1)
  {
    x = saved_x + saved_dx - dx;
  }
  // last_dx = dx;
  // last_x = x;
  // last_dy = dy;
  // last_y = y;
  last_p = p;
}

void user_init(void)
{
  /*
  os_timer_setfn - Define a function to be called when the timer fires
  void os_timer_setfn(
  os_timer_t *pTimer,
  os_timer_func_t *pFunction,
  void *pArg)
  Define the callback function that will be called when the timer reaches zero. The pTimer parameters is a pointer to the timer control structure.
  The pFunction parameters is a pointer to the callback function.
  The pArg parameter is a value that will be passed into the called back function. The callback function should have the signature:
  void (*functionName)(void *pArg)
  The pArg parameter is the value registered with the callback function.
  */
  os_timer_setfn(& myTimer, timerCallback, NULL);
  /*
  os_timer_arm -  Enable a millisecond granularity timer.
  void os_timer_arm(
  os_timer_t *pTimer,
  uint32_t milliseconds,
  bool repeat)
  Arm a timer such that is starts ticking and fires when the clock reaches zero.
  The pTimer parameter is a pointed to a timer control structure.
  The milliseconds parameter is the duration of the timer measured in milliseconds. The repeat parameter is whether or not the timer will restart once it has reached zero.
  */
  os_timer_arm(& myTimer, 10, true);
}

// End of user_init
void setup()
{
  WiFi.disconnect();
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
  delay(1);
  Serial.begin(115200);
  Serial.println();
  Serial.println();
  Serial.println("");
  Serial.println("--------------------------");
  Serial.println("ESP8266 Timer Test");
  Serial.println("--------------------------");
  user_init();
}

void loop()
{
  if (Serial.available())
  {
    sendflag = false;
    c = Serial.read();
    switch (c)
    {
      case(' '):
      {
        val[state] = constrain(data.toInt(), 0, 180);
        data = "";
        state++;
        break;
      }
      case('|'):
      {
        val[state] = constrain(data.toInt(), 0, 180);
        data = "";
        flag = true;
        sendflag = true;
        state = 0;
        break;
      }
      default:
      {
        data += c;
      }
    }
  }
  yield(); // or delay(0);
}
