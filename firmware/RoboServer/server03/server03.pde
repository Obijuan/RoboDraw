#include <skymega.h>
#include <VarSpeedServo.h>

//-- Define the commands ----------------------

//-- Cmd SERVO1:  Move the servo 1 (first link) to a given angle
//---- The angle is in degrees (double value)
#define CMD_SERVO1 'A'

//-- Cmd SERVO2: Move the servo 2 (second link) to a given angle
#define CMD_SERVO2 'B'

//-- Cmd SERVO3: Move the wrist to a given angle
#define CMD_SERVO3 'C'


//-- Cmd Velocity: change the current servo speed
#define CMD_SPEED 'V'

//-- Cmd point: Move the 2 servos at the same time
//--  (Coordinate movement) The angles are integer values
//-- Extended degrees are used (i.e 901 means 90.1 degrees)
#define CMD_POINT 'P'

VarSpeedServo forearm;
VarSpeedServo arm;
VarSpeedServo wrist;


int speed = 100;
int wspeed = 80;  //-- Wrist speed

//-- Current position
int curr_arm = 0;
int curr_forearm = 0;

void setup()
{
  // Configure the skymega led
  pinMode(LED, OUTPUT);
  
  //-- Configure the serial port
  Serial.begin(9600);
  
  //-- Configure the servos
  arm.attach(SERVO2);
  forearm.attach(SERVO4);
  wrist.attach(SERVO6);
  
  arm.slowmove(0 + 930,speed);
  forearm.slowmove(0 + 900, speed);
  wrist.slowmove(-200 + 900, wspeed);
  
  
  //delay(500); 
  digitalWrite(LED, ON);   // set the LED on
  Serial.print("Ready!\n");
  
  
}

//-- For reading the serial input
char serial_char;

//-- Buffer for storing the received commands
#define BUFSIZE 14
char buffer[BUFSIZE+1];
int buflen = 0;

bool cmd_ready=false;

//-- Servo 1 angle
int ang1=0;
int ang2=0;
int ang3=0;


//-- Position angles of the arm and forearm
//-- (in extended degrees)
int arm_pos;
int forearm_pos;

void loop()
{
  
  //-- Task: Read the information from the serial port
  
  if (Serial.available() && buflen < BUFSIZE) {
    
    //-- Read the car
    serial_char = Serial.read();
    
    //-- Detect blank caracters. They are interpreted as the end of a command    
    if (serial_char == ' ' || serial_char == '\r' || serial_char == '\n') {
      //Serial.print("Blank\n");
      
      //-- Store the end of string
      buffer[buflen]=0;
      
      //-- Now there is a command ready to be processed!
      if (buflen>0)
        cmd_ready = true;
    }
      
    //-- Normal character: store it in the buffer  
    else {
      buffer[buflen]=serial_char;
      buflen++;
      //Serial.print("OK\n");
    }
  }
  
  //-- If there is a command ready or the buffer is full
  //-- process the command!!
  if (cmd_ready || buflen==BUFSIZE) {
    
    //-- Process the command
    process_cmd();
    
    //-- Command processed!
    cmd_ready=false;
    buflen=0;
  }
 
}

void process_cmd()
{
  //-- Debugg...
  //Serial.print("CMD: ");
  //Serial.print(buffer);
  //Serial.print("---\n");
  
  switch(buffer[0]) {
    case CMD_SERVO1: 
      //-- Get the angular value
      ang1 = strtol(&buffer[1],NULL,10);
      
      arm.slowmove(ang1 + 900, speed);
      
      //-- Debug!
      //Serial.print("Servo 1: ");
      //Serial.print(ang1);
      //Serial.print("\n");
      break;
      
    case CMD_SERVO2: 
      //-- Get the angular value
      ang2 = strtol(&buffer[1],NULL,10);
      
      forearm.slowmove(ang2 + 900, speed);
      
      //-- Debug!
      //Serial.print("Servo 2: ");
      //Serial.print(ang2);
      //Serial.print("\n");
      break;  
      
    case CMD_SERVO3:
      //-- Get the angular value
      ang3 = strtol(&buffer[1],NULL,10);
      
      wrist.slowmove(ang3 + 900, wspeed);
      
      //-- Debug!
      //Serial.print("Servo 3: ");
      //Serial.print(ang3);
      //Serial.print("\n");
      break;    
      
    case CMD_SPEED: 
      //-- Get the angular value
      speed = strtod(&buffer[1],NULL);
      
      //-- Debug!
      //Serial.print("Speed: ");
      //Serial.print(speed);
      //Serial.print("\n");
      break;  
      
    case CMD_POINT:
      char * tmp;
      char *tmp2;
      
      //-- Get the angular target position
      arm_pos = strtol(&buffer[1],&tmp,10);
      
      //-- Next car should be ','
      if (tmp!=NULL) {
	if (*tmp==',') {
          tmp2 = (tmp+1);
	  forearm_pos = strtol(tmp2,NULL,10);
	  
	  //Serial.print("Point: ");
          //Serial.print(arm_pos);
          //Serial.print(", ");
          //Serial.print(forearm_pos);
          //Serial.print("\n");
	  
	  //-- If everthing is ok... move the servos!
	  to_point(arm_pos, forearm_pos);
	  //Serial.print("OK\n");
	}
      }
  }
  
}

unsigned int to_point(int a, int b)
{
  //-- Calculate the angular distance
  int d1 = abs(a - curr_arm);
  int d2 = abs(b - curr_forearm);
  
  //-- Set the new current point
  curr_arm = a;
  curr_forearm = b;
  
  if (d1>d2) {
  
    int slow = round((d2 * speed)/float(d1));
  
    arm.slowmove(-a+930,speed);
    forearm.slowmove(-b+900,slow);
  }
  else {
    int slow = round((d1 * speed)/float(d2));

		//Serial.print("Slow: ");
		//Serial.print(slow); Serial.print("\n");
  
    arm.slowmove(-a+930,slow);
    forearm.slowmove(-b+900,speed);
  }
  
}






