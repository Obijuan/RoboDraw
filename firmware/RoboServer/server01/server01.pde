#include <skymega.h>
#include <Servo.h>

//-- Define the commands ----------------------

//-- Cmd SERVO1:  Move the servo 1 (first link) to a given angle
//---- The angle is in degrees (double value)
#define CMD_SERVO1 'A'

//-- cMD SERVO2: Move the servo 2 (second link) to a given angle
#define CMD_SERVO2 'B'

Servo servo[2];

void setup()
{
  // Configure the skymega led
  pinMode(LED, OUTPUT);
  
  //-- Configure the serial port
  Serial.begin(9600);
  
  //-- Configure the servos
  servo[0].attach(SERVO2);
  servo[1].attach(SERVO4);
  
  delay(500); 
  digitalWrite(LED, ON);   // set the LED on
  Serial.print("Ready!\n");
}

//-- For reading the serial input
char serial_char;

//-- Buffer for storing the received commands
#define BUFSIZE 8
char buffer[BUFSIZE+1];
int buflen = 0;

bool cmd_ready=false;

//-- Servo 1 angle
float ang1=0;
float ang2=0;

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
  Serial.print("CMD: ");
  Serial.print(buffer);
  Serial.print("---\n");
  
  switch(buffer[0]) {
    case CMD_SERVO1: 
      //-- Get the angular value
      ang1 = strtod(&buffer[1],NULL);
      
      servo[0].write(ang1 + 90.0);
      
      //-- Debug!
      Serial.print("Servo 1: ");
      Serial.print(ang1);
      Serial.print("\n");
      break;
      
    case CMD_SERVO2: 
      //-- Get the angular value
      ang2 = strtod(&buffer[1],NULL);
      
      servo[1].write(ang2 + 90.0);
      
      //-- Debug!
      Serial.print("Servo 2: ");
      Serial.print(ang2);
      Serial.print("\n");
      break;  
  }
  
}








