/*
   Пример использования библиотеки GyverButton, 1- 2- 3- нажатие
*/
#include "GyverButton.h"

#define DIGINPUTS 2 // amount of buttons
#define ANINPUTS 2 // amount of potentiometers
#define JOYSINPUTS 0 // amount of potentiometers
int pin_input[DIGINPUTS + ANINPUTS + JOYSINPUTS] = {5,6,0,1};

GButton * butt1 = new GButton(pin_input[0]);
GButton * butt2 = new GButton(pin_input[1]);

GButton * gbutt[2] = {butt1, butt2};

int dump[DIGINPUTS + ANINPUTS + JOYSINPUTS];
int prev_dump[DIGINPUTS + ANINPUTS + JOYSINPUTS];

unsigned long timer;
int period = 50;

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
  for (int i = 0; i < JOYSINPUTS; ++i)
  {
    json += "\"";
    json += role;
    json += "_potent_";
    json += String(i+1);
    json += "\": ";
    json += String(arr[DIGINPUTS + ANINPUTS+ i]);
    json += ", ";
  }
  json[json.length() - 1] = "}";
  return json;
}
void getData ()
{
  for (int i = 0; i < DIGINPUTS + ANINPUTS; ++i)
  {
    if (i < DIGINPUTS)
    {
      dump[i] = gbutt[i]->isHold();
      if (dump[i] == 1)
      {
        Serial.println(dump[i]);
      }
      //Serial.println (dump[i]);
    }
    else
    {
      dump[i] = analogRead(pin_input[i]);
    }
  }
  /*dump[0] = butt1.isClick();
  dump[1] = butt2.isClick();
  dump[2] = analogRead(POTEN1_PIN);
  dump[3] = analogRead(POTEN2_PIN);*/
}

void arrPrint (int* arr)
{
  for (int i = 0; i < DIGINPUTS + ANINPUTS; ++i)
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
  /*butt1.tick();  // обязательная функция отработки. Должна постоянно опрашиваться
  butt2.tick();*/
  for (int i = 0; i < DIGINPUTS; ++i)
  {
    gbutt[i]->tick();
    //Serial.println("TICK");
  }
  //if (butt1->isClick()) Serial.println("Button 1");
  //if (butt2->isClick()) Serial.println("Button 2");
  
  if ((millis() - timer) > period)
  {
    getData();
    arrPrint(dump);
    Serial.println(jsonGeneration(dump));
    timer = millis();
  }
}
