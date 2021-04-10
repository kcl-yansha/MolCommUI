// -----------------------------
// ACTION.INO
//
// Include here the functions used to control and move the motors
//------------------------------

//==========
// VARIABLES
//==========

float toMove;

signed long distances_to_go[3];
signed long targets_position[3];
signed long distances_left[3];

//=================
// PUBLIC FUNCTIONS
//=================

// -----------------------------------
// Run the motors to move the syringes
void runFew() {
  
  AccelStepper steppers[3] = {stepper1, stepper2, stepper3};

  // Get the direction of the move
  int direction = 1;
  if (strcmp(dir, "B") == 0) {
    direction = -1;
  }

  // Set the direction to the distance, and apply to the motor
  for (int i = 0; i < 3; i += 1) {
    if (motors[i] == 1) {
      toMove = direction * distances[i];
      steppers[i].move(toMove);
    }
  }
  
  // Initialise the motor status for the run loop
  int stepperStatus[3] = {0, 0, 0};

  // Start the main loop
  while (array_sum(stepperStatus, 3) != array_sum(motors, 3)) {
    
    // Iteration over the 3 steppers
    for (int i = 0; i < 3; i += 1) {
      
      // Check if the stepper is selected
      if (motors[i] == 1) {
        
        // Ask the stepper to move to position at constant speed.
        if (stepperStatus[i] == 0 ) {
          steppers[i].run();
        }
        
        // Check if it reached it's position - if yes, set the status
        if (steppers[i].distanceToGo() == 0) {
          stepperStatus[i] = 1;
        }
      }
    }
    getDataFromPC();
  }
  clearVariables();
}

// -------------------
// Stop all the motors
void stopAll() {
  for (int i = 0; i < 3; i += 1) {
    steppers[i].stop();
  }
}

// -------------------------------------
// Pause all the motors to restart later
void pauseRun() {

  // Calculate the remaining distance to go
  for (int i = 0; i < 3; i += 1) {
    distances_to_go[i] = steppers[i].distanceToGo();
    targets_position[i] = steppers[i].targetPosition();
    distances_left[i] = distances_to_go[i] - distances_left[i];
    steppers[i].move(distances_to_go[i]);
  }

  // Wait for the RESUME command
  while (strcmp(mode, "RESUME") != 0) {
    getDataFromPC();
  }

  // Assign the distances to go to the new distance
  for (int i = 0; i < 3; i += 1) {
    distances[i] = distances_left[i];
  }

  // Restart the motors
  return runFew();
}
