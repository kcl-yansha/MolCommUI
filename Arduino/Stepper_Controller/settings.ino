// -----------------------------
// SETTINGS.INO
//
// Include here the functions used to modify the settings of the motors
//------------------------------

//=================
// PUBLIC FUNCTIONS
//=================


// --------------------------------
// Update the speed of the motor
void updateSpeed() {

  switch (motorID) {      
    
    // Apply speed to motor 1
    case 1:
        stepper1.setMaxSpeed(value);
      break;

    // Apply speed to motor 2
    case 2:
        stepper2.setMaxSpeed(value);
      break;

    // Apply speed to motor 3
    case 3:
        stepper3.setMaxSpeed(value);
      break;

    // Apply speed to motor 4
    case 4:
        stepper4.setMaxSpeed(value);
      break;
  }
  
  // Reset all variables
  clearVariables();
}


// --------------------------------
// Update the accel of the motor
void updateAccel() {
  
  switch (motorID) {

    // Apply accel to motor 1
    case 1:
        stepper1.setAcceleration(value);
      break;

    // Apply accel to motor 2
    case 2:
        stepper2.setAcceleration(value);
      break;

    // Apply accel to motor 3
    case 3:
        stepper3.setAcceleration(value);
      break;

    // Apply accel to motor 4
    case 4:
        stepper4.setAcceleration(value);
      break;
  }
  
  // Reset all variables
  clearVariables();
}



// ------------------------------------
// Clear all variables after the action
void clearVariables() {

  memset(mode,0,sizeof(mode));
  motorID = 0;
  value = 0.0;

}
