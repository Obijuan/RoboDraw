//--------------------------------------------------------------
//-- ArduSnake library: Locomotion of modular snake robots
//-----------------------------------------------------------
//-- Layer: Oscillator
//------------------------------------------------------------
//-- Example of use of the Oscillator layer
//--
//-- Example 3: Two servos oscillating independenly, with different
//--  parameters
//--------------------------------------------------------------
//-- (c) Juan Gonzalez-Gomez (Obijuan), Feb-2012
//-- GPL license
//--------------------------------------------------------------
#include <VarSpeedServo.h>
#include "skymega.h"

VarSpeedServo forearm;
VarSpeedServo arm;

const int speed = 25;

void setup()
{
 
  forearm.attach (SERVO2);
  arm.attach (SERVO4);

}

void loop()
{
  forearm.slowmove(0 +90, speed);
  arm.slowmove(-60 +90, speed);
  delay(2200);
  
  arm.slowmove(40 +90, speed);
  delay(1650);
  
  arm.slowmove(90 +90, speed);
  forearm.slowmove(-90 + 90, speed);
  delay(1400);
  
  arm.slowmove(-45 + 90, speed);
  delay(2300);
}


