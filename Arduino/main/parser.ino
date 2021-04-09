// -----------------------------
// PARSER.INO
//
// Include here the functions used to read the communication from the computer
//------------------------------

// VARIABLES

const char startMarker = '<';
const char endMarker = '>';

boolean readInProgress = false;

// PUBLIC FUNCTIONS

// Read the serial port and extract commands from it
void getDataFromPC() {
  
  // Check if data is coming through the serial port
  if (Serial.available() > 0){

    // Read the entry
    String x = Serial.readStringUntil(endMarker);

    if (x.charAt(0) == startMarker && x.indexOf('\n') < 0){
      Serial.println(x);
    }
  }
}
