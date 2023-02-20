// -----------------------------
// PARSER.INO
//
// Include here the functions used to read the communication from the computer
//------------------------------

//==========
// VARIABLES
//==========

const char startMarker = '<';
const char endMarker = '>';

byte bytesRecvd = 0;

//=================
// PUBLIC FUNCTIONS
//=================

// -------------------------------------------------
// Read the serial port and extract commands from it
void getDataFromPC() {
  
  // Check if data is coming through the serial port
  if (Serial.available() > 0)
  {

    // Read the next incoming character
    char x = Serial.read();

    // Detect the end marker and call the parser - Needs to be 1st if statement
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      
      // Clear the buffer
      inputBuffer[bytesRecvd] = 0;
      
      return parseData();
    }

    // Save the current character in memory - Needs to be 2nd if statement
    if (readInProgress) {
      
      // Add the character to the buffer
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;

      // Correct if size is exceeding buffer size
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    // Detect the start marker and collect characters - Needs to be 3rd if statement
    if (x == startMarker) {
      bytesRecvd = 0;
      readInProgress = true;
    }
    
  }
}

// -----------------------
// Parse the incoming data
void parseData() {

  char * strtokIndx; // this is used by strtok() as an index

  // Extract the MODE
  strtokIndx = strtok(inputBuffer, ",");
  strcpy(mode, strtokIndx);

  // Extract the MOTORID
  strtokIndx = strtok(NULL, ",");
  String motorstr(strtokIndx);

  // Convert into an integer
  motorID = atoi(strtokIndx);

  // Extract the VALUE 
  strtokIndx = strtok(NULL, ",");
  value = atof(strtokIndx);

  // Communicate back to the computer
  newDataFromPC = true;

}



// ------------------------------
// Select the function to execute
void executeThisFunction() {
  
  // Go to the SPEED setting function
  if (strcmp(mode, "SPEED") == 0) {
    replyToPC();
    updateSpeed();
  }

  // Go to the ACCEL setting function
  else if (strcmp(mode, "ACCEL") == 0) {
    replyToPC();
    updateAccel();
  }

  // Go to the RUN function
  else if (strcmp(mode, "RUN") == 0) {
    replyToPC();
    runFew();
  }

  // Go to the STOP function
  else if (strcmp(mode, "STOP") == 0) {
    replyToPC();
    stopAll();
  }

  // Go to the POS function
  else if (strcmp(mode, "POSITION") == 0) {
    positionCheck();
  }

  // Go to the GETID function
  else if (strcmp(mode, "GETID") == 0) {
    returnID();
  }
}


// ------------------------------------
// Return the distance left to the computer
void positionCheck() {

  switch (motorID) {

    // Check the left distance for motor 1
    case 1:
        distanceleft=stepper1.distanceToGo();
      break;

    // Check the left distance for motor 2
    case 2:
        distanceleft=stepper2.distanceToGo();
      break;

    // Check the left distance for motor 3
    case 3:
        distanceleft=stepper3.distanceToGo();
      break;

    // Check the left distance for motor 4
    case 4:
        distanceleft=stepper4.distanceToGo();
      break;
  }

  Serial.print("<");
  Serial.print(distanceleft);
  Serial.println(">");
  
  // Reset all variables
  clearVariables();
}


// ------------------------------------
// Return the Device ID to the computer
void returnID() {
  Serial.println(DEVICEID);
  newDataFromPC = false;
  clearVariables();
}


// ---------------------------------------------------
// Reply to the computer to aknowledge the new command
void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<mode: ");
    Serial.print(mode);
    Serial.print(", motorID: ");
    Serial.print(motorID);
    Serial.print(", value: ");
    Serial.print(value);
    Serial.println(">");
  }
  
}
