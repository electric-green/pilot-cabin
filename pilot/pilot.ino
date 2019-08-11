#include "GyverButton.h"

#define DIGINPUTS 0 // amount of buttons
#define ANINPUTS 1 // amount of potentiometers
#define JOYSINPUTS 2 // amount of joysticck axis
int pin_input[DIGINPUTS + ANINPUTS + JOYSINPUTS] = {2,0,1};

GButton * butt1 = new GButton(pin_input[0]);
GButton * butt2 = new GButton(pin_input[1]);

GButton * gbutt[2] = {butt1, butt2};

int dump[DIGINPUTS + ANINPUTS + JOYSINPUTS];
int prev_dump[DIGINPUTS + ANINPUTS + JOYSINPUTS];

unsigned long timer;
int period = 200;

String role = "pilot";

String jsonGeneration(int* arr)
{
  String json = "{";
  for (int i = 0; i < DIGINPUTS; ++i)
  {
    json += "\"";
    json += role;
    json += "_butt_";
    json += String(i+1);
    json += "\": ";
    json += String(arr[i]);
    json += ", ";
  }
  for (int i = 0; i < ANINPUTS; ++i)
  {
    json += "\"";
    json += role;
    json += "_potent_";
    json += String(i+1);
    json += "\": ";
    json += String(arr[DIGINPUTS + i]);
    json += ", ";
  }
  /*for (int i = 0; i < JOYSINPUTS; ++i)
  {
    json += "\"";
    json += role;
    json += "_joys_";
    json += String(i+1);
    json += "\": ";
    json += String(arr[DIGINPUTS + ANINPUTS+ i]);
    json += ", ";
  }*/
  if (JOYSINPUTS)
  {
    json += "\"";
    json += role;
    json += "_joys_";
    json += String('1');
    json += "\": [";
    for (int i = 0; i < JOYSINPUTS; ++i)
    {
      json += String(arr[DIGINPUTS + ANINPUTS+ i]);
      json += ", ";
    }
    json[json.length() - 2] = ']';
    json[json.length() - 1] = '}';
  }
  //json[json.length() - 2] = '}';
  //json.remove(json.length() - 1);
  return json;
}
void getData ()
{
  for (int i = 0; i < DIGINPUTS + ANINPUTS + JOYSINPUTS; ++i)
  {
    if (i < DIGINPUTS)
    {
      dump[i] = gbutt[i]->isHolded();
    }
    else if (i < DIGINPUTS + ANINPUTS)
    {
      dump[i] = analogRead(pin_input[i]);
    }
    else
    {
      dump[i] = analogRead(pin_input[i]);
      //dump[i] = (-1) * map(dump[i], 0, 1023, -1, 1);
      //Serial.println("JOYS");
      //Serial.println(dump[i]);
      if (dump[i] <= 50)
      {
        dump[i] = -1;
      }
      if ((dump[i] > 50) && (dump[i] < 950))
      {
        dump[i] = 0;
      }
      if (dump[i] >= 950)
      {
        dump[i] = 1;
      }
    }
  }
}

void arrPrint (int* arr)
{
  for (int i = 0; i < DIGINPUTS + ANINPUTS + JOYSINPUTS; ++i)
  {
    Serial.print(arr[i]);
    Serial.print(",");
  }
  Serial.println();
}
void copy(int* arr1,int* arr2)
{
  for(int i = 0; i < DIGINPUTS + ANINPUTS; ++i)
  {
    arr1[i] = arr2[i];
  }
}

void setup() {
  Serial.begin(115200);
  timer = millis();
  butt1->setTimeout(1);
  butt2->setTimeout(1);
}

void loop() {

  for (int i = 0; i < DIGINPUTS; ++i)
  {
    gbutt[i]->tick();
  }
  //if (butt1->isClick()) Serial.println("Button 1");
  //if (butt2->isClick()) Serial.println("Button 2");
  
  if ((millis() - timer) > period)
  {
    getData();
    //arrPrint(dump);
    Serial.println(jsonGeneration(dump));
    timer = millis();
  }
}
