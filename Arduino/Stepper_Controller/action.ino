// -----------------------------
// ACTION.INO
//
// Include here the functions used to control and move the motors
//------------------------------


//=================
// PUBLIC FUNCTIONS
//=================

// -----------------------------------
// Run the motors to move the syringes
void runFew() {
  
  switch (motorID) {

    // Apply target position to motor 1
    case 1:
        stepper1.move(value);
      break;

    // Apply target position to motor 2
    case 2:
        stepper2.move(value);
      break;

    // Apply target position to motor 3
    case 3:
        stepper3.move(value);
      break;

    // Apply target position to motor 4
    case 4:
        stepper4.move(value);
      break;
  }
  clearVariables();
  
}



// This new function will run the motors if the motors need to
void checkAndRun() {
    
    if (stepper1.distanceToGo()!= 0){ 
      stepper1.run();
    }
    if (stepper2.distanceToGo()!= 0){ 
      stepper2.run();
    }
    if (stepper3.distanceToGo()!= 0){ 
      stepper3.run();
    }
    if (stepper4.distanceToGo()!= 0){ 
      stepper4.run();
    }
    
}


// -------------------
// Stop all the motors
void stopAll() {

  switch (motorID) {

    // Stop motor 1
    case 1:
        stepper1.move(0);
      break;

    // Stop motor 2
    case 2:
        stepper2.move(0);
      break;

    // Stop motor 3
    case 3:
        stepper3.move(0);
      break;

    // Stop motor 4
    case 4:
        stepper4.move(0);
      break;
  }
  clearVariables();
}
