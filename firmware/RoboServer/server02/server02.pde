#include <skymega.h>
#include <VarSpeedServo.h>

//-- Define the commands ----------------------

//-- Cmd SERVO1:  Move the servo 1 (first link) to a given angle
//---- The angle is in degrees (double value)
#define CMD_SERVO1 'A'

//-- Cmd SERVO2: Move the servo 2 (second link) to a given angle
#define CMD_SERVO2 'B'

//-- Cmd Velocity: change the current servo speed
#define CMD_SPEED 'V'

//-- Cmd point: Move the 2 servos at the same time
//--  (Coordinate movement) The angles are integer values
//-- Extended degrees are used (i.e 901 means 90.1 degrees)
#define CMD_POINT 'P'

VarSpeedServo servo[2];

VarSpeedServo forearm;
VarSpeedServo arm;


int speed = 50;

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
  
  arm.slowmove(0 + 900,speed);
  forearm.slowmove(0 + 900, speed);
  
  
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
float ang1=0;
float ang2=0;


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
      ang1 = strtod(&buffer[1],NULL);
      
      servo[0].slowmove(ang1 + 90.0, speed);
      
      //-- Debug!
      //Serial.print("Servo 1: ");
      //Serial.print(ang1);
      //Serial.print("\n");
      break;
      
    case CMD_SERVO2: 
      //-- Get the angular value
      ang2 = strtod(&buffer[1],NULL);
      
      servo[1].slowmove(ang2 + 90.0, speed);
      
      //-- Debug!
      //Serial.print("Servo 2: ");
      //Serial.print(ang2);
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

const float tw=0.45;

//-- Coordinated movement
int to_point(int a, int b)
{
  //-- Calculate the angular distance
  int d1 = abs(a - curr_arm);
  int d2 = abs(b - curr_forearm);
  
  //Serial.print("d1: ");
  //Serial.print(d1);
  //Serial.print(" d2: ");
  //Serial.print(d2);
  //Serial.print("\n");
  
  //-- Set the new current point
  curr_arm = a;
  curr_forearm = b;
  
  
  if (d1>d2) {
    unsigned int slow = unsigned(d2 * speed)/d1;
    
    Serial.print("Slow: ");
    Serial.println(slow);
    
  
    arm.slowmove(a+900,speed);
    forearm.slowmove(b+900,slow);
    return round(tw*d1*100.0/speed);
  }
  else {
    unsigned int slow = unsigned(d1 * speed)/d2;
  
    arm.slowmove(a+900,slow);
    forearm.slowmove(b+900,speed);
    return round(tw*d2*100.0/speed);
  }
  
}







