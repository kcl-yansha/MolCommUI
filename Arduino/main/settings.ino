// -----------------------------
// SETTINGS.INO
//
// Include here the functions used to modify the settings of the motors
//------------------------------

//==========
// VARIABLES
//==========

float jog1Delta;
float jog2Delta;
float jog3Delta;

//=================
// PUBLIC FUNCTIONS
//=================

// -------------------------------------
// Select which motors need to be edited
void toggleMotors( String motorstr ) {

  motors[0] = 0;
  motors[1] = 0;
  motors[2] = 0;

  if(motorstr.indexOf("1") >= 0) {
    motors[0] = 1;
  }
  if(motorstr.indexOf("2") >= 0) {
    motors[1] = 1;
  }
  if(motorstr.indexOf("3") >= 0) {
    motors[2] = 1;
  }  
}

// --------------------------------
// Update the settings of the motor
void udpateSettings() {

  // Re-initialise the current position
  stepper1.setCurrentPosition(0.0);
  stepper2.setCurrentPosition(0.0);
  stepper3.setCurrentPosition(0.0);

  switch (motorID) {

    // Apply settings to motor 1
    case 1:

      // Change max speed
      if (strcmp(setting, "SPEED") == 0) {
        stepper1.setMaxSpeed(value);
      }

      // Change acceleration
      else if (strcmp(setting, "ACCEL") == 0) {
        stepper1.setAcceleration(value);
      }

      // Change jog delta value
      else if (strcmp(setting, "DELTA") == 0) {
        jog1Delta = value;
      }
      break;

    // Apply settings to motor 2
    case 2:

      // Change max speed
      if (strcmp(setting, "SPEED") == 0) {
        stepper2.setMaxSpeed(value);
      }

      // Change acceleration
      else if (strcmp(setting, "ACCEL") == 0) {
        stepper2.setAcceleration(value);
      }

      // Change jog delta value
      else if (strcmp(setting, "DELTA") == 0) {
        jog2Delta = value;
      }
      break;

    // Apply settings to motor 3
    case 3:

      // Change max speed
      if (strcmp(setting, "SPEED") == 0) {
        stepper3.setMaxSpeed(value);
      }

      // Change acceleration
      else if (strcmp(setting, "ACCEL") == 0) {
        stepper3.setAcceleration(value);
      }

      // Change jog delta value
      else if (strcmp(setting, "DELTA") == 0) {
        jog3Delta = value;
      }
      break;
  }

  // Reset all variables
  clearVariables();
}

// ------------------------------------
// Clear all variables after the action
void clearVariables() {
  
  char messageFromPC[buffSize] = {0};
  char mode[buffSize] = {0};
  char setting[buffSize] = {0};
  int motorID = 0;
  float value = 0.0;
  char dir[buffSize] = {0};

  float p1_optional = 0.0;
  float p2_optional = 0.0;
  float p3_optional = 0.0;
  
}
