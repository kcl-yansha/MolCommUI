###========================================================###
### MolCommUI --- v1.0                                     ###
### Date: 20/02/2023                                       ###
###========================================================###
# Disclaimer: Python3 software developed by the Yansha Group #
#             at King's College London (UK)                  #
# Link: https://www.yanshadeng.org                           #
#------------------------------------------------------------#
# Author(s):                                                 #
# - Vivien WALTER (walter.vivien@gmail.com)                  #
###========================================================###

import time

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# --------------------------------------------
# Return the axis/motor ID from the input axis
def _get_axis_ID(axis):

    # Define the axis dict
    axis_2_id = {
    'X':'1',
    'Y':'2',
    'Z':'3',
    'A':'4',
    }

    return axis_2_id[axis]

# ----------------------------------------------
# Read the message coming from the board, if any
def _read_message(board, timeout=1):

    # Define the markers
    startMarker = 60 # <
    endMarker = 62 # >
    midMarker = 44 # ,

    final_string = ""
    x = "z" # Random char to start with

    # Start a timer
    start_time = time.time()
    read_arduino = True

    # Wait for the start character
    while  ord(x) != startMarker and read_arduino:
        x = board.read()

        # Check for empty character
        try:
            test_x = ord(x)
        except:
            x = "z"

        # Check for timeout
        if timeout > 0 and time.time() - start_time >= timeout:
            read_arduino = False

    # Start the processing loop
    while ord(x) != endMarker and read_arduino:

        # Get the next character
        x = board.read()

        # Start the reading process
        if ord(x) != startMarker and ord(x) != endMarker:
            final_string += x.decode()

        # Check for timeout
        if timeout > 0 and time.time() - start_time >= timeout:
            read_arduino = False

    # Return a timeout error if needed
    if not read_arduino:
        final_string = None

    return final_string

# ----------------------
# Request the syringe ID
def _request_syringe_ID(board, verbose=True):

    # Get the command
    if verbose:
        sendStr = "<GETID,0,0.0>"
        print(board.name + ': Sending ' + sendStr)

    # Send the command to the Arduino
    board.write(sendStr.encode())
    board.flushInput()

    # Wait for the answer
    while board.inWaiting() == 0:
        pass

    # Read the answer
    text_from_arduino = _read_message(board)

    return text_from_arduino

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------------------
# Return the axis/motor ID from the input axis
def getAxisID(axis):

    # Define the axis dict
    axis_2_id = {
    'X':'1',
    'Y':'2',
    'Z':'3',
    'A':'4',
    }

    return axis_2_id[axis]

# --------------------------------
# Read any output from the Arduino
def readFromArduino(board, timeout=-1):

    # Start a timer
    start_time = time.time()
    read_arduino = True

    # Start the waiting loop
    while board.inWaiting() == 0 and read_arduino:

        # Check for timeout
        if timeout > 0 and time.time() - start_time >= timeout:
            read_arduino = False

    # Read the incoming message
    if read_arduino:
        return _read_message(board)

    else:
        return None

# -----------------------------------------
# Check the syringe group at the given port
def checkSyringeBoard(board, verbose=True):

    # Send the message
    if verbose:
        print(board.name + ': Reading ID...' )

    return _request_syringe_ID(board, verbose=verbose)

# -------------------------------------
# Apply the settings to the given board
#def editSettings(board, value, type='speed', axis='X', verbose=True):
def editSettings(pump, value, type='speed', axis='X', verbose=True):

    # Get the board
    board = pump.syringe_group.board

    # Get the axis ID
    motorID = _get_axis_ID(axis)

    # Get the command
    sendStr = "<"+type.upper()+","+motorID+","+str(value)+">"
    if verbose:
        print(board.name + ': Sending ' + sendStr)

    # Send the command to the Arduino
    board.write(sendStr.encode())
    board.flushInput()

    # Wait for the answer
    while board.inWaiting() == 0:
        pass

    # Read the answer
    text_from_arduino = _read_message(board)

    # Change the status of the pump
    pump.equipment.is_updated = True

    return text_from_arduino

# -----------------------------------
# Run the syringe for the given value
def runSyringe(syringe, board, value, axis='X', verbose=True):

    # Get the axis ID
    motorID = _get_axis_ID(axis)

    # Get the command
    sendStr = "<RUN,"+motorID+','+str(value)+'>'
    if verbose:
        print(board.name + ': Sending ' + sendStr)

    # Send the command to the Arduino
    board.write(sendStr.encode())
    board.flushInput()

    # Wait for the answer
    while board.inWaiting() == 0:
        pass

    # Read the answer
    text_from_arduino = _read_message(board)

    # Start the check pattern
    if text_from_arduino is not None:

        # Toggle the status of the motor
        syringe.is_running = True
        syringe.updateRunning()

        # Send the check command
        syringe.check()

    return text_from_arduino

# ---------------------
# Interrupt the syringe
def stopSyringe(syringe, board, axis='X', verbose=True):

    # Get the axis ID
    motorID = _get_axis_ID(axis)

    # Get the command
    sendStr = "<STOP,"+motorID+',0.0>'
    if verbose:
        print(board.name + ': Sending ' + sendStr)

    # Send the command to the Arduino
    board.write(sendStr.encode())
    board.flushInput()

    # Read the answer
    text_from_arduino = _read_message(board)

    # Toggle the status of the motor
    syringe.is_running = False
    syringe.updateRunning()

    return text_from_arduino

# ---------------------------------
# Check the progress of the syringe
def checkProgress(syringe, board, axis='X', verbose=True):

    # Get the axis ID
    motorID = _get_axis_ID(axis)

    # Get the command
    sendStr = "<POSITION,"+motorID+',0.0>'
    if verbose:
        print(board.name + ': Sending ' + sendStr)

    # Send the command to the Arduino
    board.write(sendStr.encode())
    board.flushInput()

    # Read the answer
    text_from_arduino = _read_message(board)

    # Send another check
    if text_from_arduino is not None:

        # Save the remaining value
        #print(text_from_arduino)

        # Start the next check
        syringe.check()

    return ['check', axis, text_from_arduino]
