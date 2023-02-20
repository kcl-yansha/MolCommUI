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

import serial
import serial.tools.list_ports

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------------------------------------
# Return the list of all COM (USB) ports connected to the computer
def get_list_ports():

    # Get the list of ports
    ports = serial.tools.list_ports.comports()

    # Make the list
    all_ports = []
    for p in ports:
        all_ports.append(p.device)

    return all_ports

# ------------------------------------
# Start a connection to the given port
def start_connection(port, baudrate):

    # Start the connection
    connection = serial.Serial()

    connection.port = port # Set port
    connection.baudrate = baudrate # Set baudrate

    connection.parity = serial.PARITY_NONE # Enable parity checking
    connection.stopbits = serial.STOPBITS_ONE # Number of stop bits
    connection.bytesize = serial.EIGHTBITS # Number of databits

    connection.timeout = 1 # Set a timeout value
    connection.xonxoff = 0 # Disable software control
    connection.rtscts = 0 # Disable RTS/CTS control

    # Connect to the pump
    try:
        connection.open()
        return connection

    except:
        return None

# --------------------
# Close the connection
def stop_connection(board):
    board.close()
