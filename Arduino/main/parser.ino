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

boolean readInProgress = false;
boolean newDataFromPC = false;

//=================
// PUBLIC FUNCTIONS
//=================

// -------------------------------------------------
// Read the serial port and extract commands from it
void getDataFromPC() {
  
  // Check if data is coming through the serial port
  if (Serial.available() > 0){

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

  // Extract the SETTING
  strtokIndx = strtok(NULL, ",");
  strcpy(setting, strtokIndx);

  // Extract the MOTORID
  strtokIndx = strtok(NULL, ",");
  String motorstr(strtokIndx);

  // Convert into an integer
  motorID = atoi(strtokIndx);

  // Enable the motors
  toggleMotors(motorstr);

  // Extract the VALUE
  strtokIndx = strtok(NULL, ",");
  value = atof(strtokIndx);

  // Extract the DIRECTION
  strtokIndx = strtok(NULL, ",");
  strcpy(dir, strtokIndx);

  // Extract the OPTIONAL values
  strtokIndx = strtok(NULL, ","); 
  p1_optional = atof(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  p2_optional = atof(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  p3_optional = atof(strtokIndx);

  // Set the distance values
  distances[0] = p1_optional;
  distances[1] = p2_optional;
  distances[2] = p3_optional;

  // Correct the distances in RUN mode
  if (strcmp(setting, "RUN") == 0) {
    distances[0] = 999999.0;
    distances[1] = 999999.0;
    distances[2] = 999999.0;
  }

  // Communicate back to the computer
  newDataFromPC = true;
  replyToPC();

  // Execute the selected function
  return executeThisFunction();
  
}

// ------------------------------
// Select the function to execute
void executeThisFunction() {
  
  // Go to the RUN function
  if (strcmp(mode, "RUN") == 0) {

    // Check the the SETTING is always set to DIST before proceeding
    if (strcmp(setting, "DIST") == 0) {
      Serial.println("I will run now");
    }
  }

  // Go to the SETTING function
  else if (strcmp(mode, "SETTING") == 0) {
    Serial.println("I will edit the settings now");
  }

  // Go to the STOP function
  else if (strcmp(mode, "STOP") == 0) {

  }

  // Go to the PAUSE function
  else if (strcmp(mode, "PAUSE") == 0) {
    
  }

  // Go to the RESUME function
  else if (strcmp(mode, "RESUME") == 0) {
    
  }

  // Go to the GETID function
  else if (strcmp(mode, "GETID") == 0) {
    return returnID();
  }

}

// ---------------------------------------------------
// Reply to the computer to aknowledge the new command
void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<mode: ");
    Serial.print(mode);
    Serial.print(" ,setting: ");
    Serial.print(setting);
    Serial.print(" ,motorID: ");
    Serial.print(motorID);
    Serial.print(" ,value: ");
    Serial.print(value);
    Serial.print(" ,direction: ");
    Serial.print(dir);
    Serial.print(" ,p1 optional: ");
    Serial.print(p1_optional);
    Serial.print(" ,p2 optional: ");
    Serial.print(p2_optional);
    Serial.print(" ,p3 optional: ");
    Serial.print(p3_optional);
    //Serial.print(" ,Time ");
    //Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
  
}

// ------------------------------------
// Return the Device ID to the computer
void returnID() {
  Serial.println(DEVICEID);
}
