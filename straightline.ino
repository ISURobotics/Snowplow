const byte numChars = 32;
char receivedChars[numChars];
char xchars[numChars];
char ychars[numChars];
char zchars[numChars];
char lastchar = 'x';

boolean newData = false;

//Code by Reichenstein7 (thejamerson.com)

//Keyboard Controls:
//
// 1 -Motor 1 Left
// 2 -Motor 1 Stop
// 3 -Motor 1 Right
//
// 4 -Motor 2 Left
// 5 -Motor 2 Stop
// 6 -Motor 2 Right

// Declare L298N Dual H-Bridge Motor Controller directly since there is not a library to load.

// Motor 1
int dir1PinA = 2;
int dir2PinA = 3;
int speedPinA = 9; // Needs to be a PWM pin to be able to control motor speed

// Motor 2
int dir1PinB = 4;
int dir2PinB = 5;
int speedPinB = 10; // Needs to be a PWM pin to be able to control motor speed

int state = 0; //Let's define states as 0 for garage moving to path, 1 for going down path to end, 2 for turning around, 3 for going back to beginning of path, 4 for going to garage



void MLForward(int speed){
  analogWrite(speedPinA, speed);//Sets speed variable via PWM 
  digitalWrite(dir1PinA, LOW);
  digitalWrite(dir2PinA, HIGH);
}

void MLStop(){
  analogWrite(speedPinA, 0);
  digitalWrite(dir1PinA, LOW);
  digitalWrite(dir2PinA, HIGH);
}

void MLReverse(int speed){
  analogWrite(speedPinA, speed);
  digitalWrite(dir1PinA, HIGH);
  digitalWrite(dir2PinA, LOW);
}

void MRForward(int speed){
  analogWrite(speedPinB, speed);//Sets speed variable via PWM 
  digitalWrite(dir1PinB, LOW);
  digitalWrite(dir2PinB, HIGH);
}

void MRStop(){
  analogWrite(speedPinB, 0);
  digitalWrite(dir1PinB, LOW);
  digitalWrite(dir2PinB, HIGH);
}

void MRReverse(int speed){
  analogWrite(speedPinB, speed);
  digitalWrite(dir1PinB, HIGH);
  digitalWrite(dir2PinB, LOW);
}


void setup() {
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(dir1PinA, OUTPUT);
  pinMode(dir2PinA, OUTPUT);
  pinMode(speedPinA, OUTPUT);
  pinMode(dir1PinB, OUTPUT);
  pinMode(dir2PinB, OUTPUT);
  pinMode(speedPinB, OUTPUT);
}

void loop() {
  recvWithStartEndMarkers();
  showNewData();
}

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  // if (Serial.available() > 0) {
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        if(rc == 'x'){
          lastchar = 'x';
          ndx = 0;
          continue;
        }
        if(rc == 'y'){
          xchars[ndx]='\0';
          lastchar = 'y';
          ndx = 0;
          continue;
        }
        if(rc == 'z'){
          ychars[ndx]='\0';
          lastchar = 'z';
          ndx = 0;
          continue;
        }
        if(lastchar == 'x'){
          xchars[ndx] = rc;
          ndx++;
        }
        if(lastchar == 'y'){
          
          ychars[ndx] = rc;
          ndx++;
        }
        if(lastchar == 'z'){
          zchars[ndx] = rc;
          ndx++;
        }
//        receivedChars[ndx] = rc;
//        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        zchars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}
String part1;
String part2;
String part3;
int speedL = 0;
int speedR = 0;
float distance = 0.0;
float xpos = 0.0;

//If x is negative, turn left.  If x is positive, turn right

void leftTurn(){
 MLForward(0);
 MRForward(150);
}

void rightTurn(){
  MLForward(150);
  MRForward(0);
}

void straight(){
  MRForward(200);
  MLForward(200);
}

void STOP(){
 MRStop();
 MLStop();
}

void showNewData() {
  if (newData == true) {
    xpos = atof(xchars);
    ypos = atof(ychars);
    zpos = atof(zchars);
    distance = atof(zchars);
    if(xpos<-5){
      leftTurn();
    }
    else if(xpos>5){
      rightTurn();
    }
    else{
      straight();
    }
    
    if(distance<30){
      STOP();
    }
    Serial.print("This just in ... ");
    Serial.println(xchars);
    //Serial.println(ychars);
    //Serial.println(zchars);
    newData = false;
  }
}

