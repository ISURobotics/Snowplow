
/* This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. */

#include <Servo.h>

//User configuration:
int percent = 0;  //between -100 and 100, indicates how fast the motor 
      //will be moving when the arduino boots
int pins[] = {5, 6}; //the signal output pins (as many as you'd like)
int inputPins[] = {2,3};
volatile int pwm_val_left = 0;
volatile int prev_time_left = 0;
volatile int pwm_val_right = 0;
volatile int prev_time_right = 0;
int enablePin12 = 0;
const int arraySize = sizeof(pins)/sizeof(int);
const int inputSize = sizeof(pins)/sizeof(int);
Servo controllers[arraySize];

void setup() {
  Serial.begin(9600);
  Serial.println("you called, master?\n");
  for (int i=0; i<arraySize; i++)
    controllers[i].attach(pins[i]); //associate the object to a pin
  attachInterrupt(digitalPinToInterrupt(2),risingRight, RISING);
  attachInterrupt(digitalPinToInterrupt(3),risingLeft, RISING);
 // attachInterrupt(digitalPinToInterrupt(18),risingEnable, RISING);
  delay(1000);
  Serial.println("type in a percent, and I will output your PWM.\n");
  
}

void risingRight(){
  attachInterrupt(digitalPinToInterrupt(2),fallingRight,FALLING);
  prev_time_right = micros();
}
void risingLeft(){
  attachInterrupt(digitalPinToInterrupt(3),fallingLeft,FALLING);
  prev_time_left = micros();
}
void fallingRight(){
  attachInterrupt(digitalPinToInterrupt(2),risingRight, RISING);
  pwm_val_right = micros()-prev_time_right;
}
void fallingLeft(){
  attachInterrupt(digitalPinToInterrupt(3),risingLeft, RISING);
  pwm_val_left = micros()-prev_time_left;
}

int leftPWMin = 0;
int rightPWMin = 0;
bool enableMotors = true;

void loop() {
  //enablePin12 = digitalRead(12);
  if(abs(pwm_val_left-1500)>100||abs(pwm_val_right-1500)>100){
  //if(abs(pwm_val_enable-1500)>100){
    controllers[0].writeMicroseconds(pwm_val_left);
    controllers[1].writeMicroseconds(pwm_val_right);
    //enableMotors = false;
    
  }
  else{
        //controllers[0].writeMicroseconds(1600);
        //controllers[1].writeMicroseconds(1600);
    int PWMvalue = percent * 5 + 1500; //scale up to 1000-2000
      
        for (int i=0; i<arraySize; i++)
          controllers[i].writeMicroseconds(PWMvalue);
      
        if (Serial.available() > 1) {
          long proposedValue = Serial.parseInt();
          if (proposedValue == 0) {
            Serial.println("ah... stop!  yes, right on it.");
            percent = 0;
          } else if (proposedValue >= -100 && proposedValue <= 100) {
            percent = proposedValue;
            Serial.print("of course. value set to ");
            Serial.print(percent);
            Serial.println("%");
          } else {
            Serial.println("oh dear. that won't do.");
          }
        }
  }
  
      //Serial.println(pwm_val_enable);  
}

