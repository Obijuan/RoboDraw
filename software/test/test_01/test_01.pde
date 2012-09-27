//--------------------------------------------------------------
//-- Set the position of all the servos to 90 degrees
//-- It is very useful for calibrating the Y1/MY1/REPY1 modules. This
//-- position correspond with the home state of the module (where the body
//-- and head plates are paralell)
//--------------------------------------------------------------
//-- (c) Juan Gonzalez-Gomez (Obijuan), Dec 2011
//-- GPL license
//--------------------------------------------------------------

#include <Servo.h> 

//-- Mapping between the servo name (in the skymega board) and the
//-- arduino pins
const int SERVO2 = 8;
const int SERVO4 = 9;
const int SERVO6 = 10;
const int SERVO8 = 11;

//-- Array for accesing the 4 servos
Servo myservo[4];  
 
void setup() 
{
  //-- Attaching the 4 servos
  myservo[0].attach(SERVO2);
  myservo[1].attach(SERVO4);
  myservo[2].attach(SERVO6);
  myservo[3].attach(SERVO8);
}  
 
void loop() 
{ 
  myservo[0].write(90);
  myservo[1].write(90);
  myservo[2].write(90);
  myservo[3].write(90);
} 
