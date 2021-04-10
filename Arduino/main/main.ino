#include <AccelStepper.h>

//==========
// VARIABLES
//==========

// ------------------------
// Global variables - fixed

// Define the pins for each motor
#define X_DIR 5
#define X_STP 2

#define Y_DIR 6
#define Y_STP 3

#define Z_DIR 7
#define Z_STP 4

// Define the constants for the motors
#define X_SPEED 1000 // X steps per second
#define Y_SPEED 1000 // Y
#define Z_SPEED 1000 // Z

#define X_ACCEL 5000.0 // X steps per second per second
#define Y_ACCEL 5000.0 // Y
#define Z_ACCEL 5000.0 // Z

// Define the baud rate of the Arduino
#define BAUD_RATE 230400

#define DEVICEID "ArduinoSyringePump - #2021-001"

// ---------------
// Motor variables

int motorID = 0;
int motors[3] = {0,0,0};

AccelStepper stepper1(AccelStepper::DRIVER, X_STP, X_DIR);
AccelStepper stepper2(AccelStepper::DRIVER, Y_STP, Y_DIR);
AccelStepper stepper3(AccelStepper::DRIVER, Z_STP, Z_DIR);

AccelStepper steppers[3] = {stepper1, stepper2, stepper3};

// -----------------------
// Communication variables

const byte buffSize = 64;

char inputBuffer[buffSize];

char mode[buffSize] = {0};
char setting[buffSize] = {0};
float value = 0.0;
char dir[buffSize] = {0};
float p1_optional;
float p2_optional;
float p3_optional;

// ----------------
// Action variables

float distances[3];

//=================
// PUBLIC FUNCTIONS
//=================

// ----------------------------------------------------
// Function called once to initialise the Arduino board
void setup() {
  
  // Initialise the baud rate of the Serial port
  Serial.begin(BAUD_RATE);

  // Set the initial max speed of the system
  stepper1.setMaxSpeed(X_SPEED);
  stepper2.setMaxSpeed(Y_SPEED);
  stepper3.setMaxSpeed(Z_SPEED);

  // Set the acceleration of the system
  stepper1.setAcceleration(X_ACCEL);
  stepper2.setAcceleration(Y_ACCEL);
  stepper3.setAcceleration(Z_ACCEL);
}

// ---------------------------------------------
// Function called repeatedly to run the Arduino
void loop() {

  // Get the data from the PC
  getDataFromPC();
  
}
