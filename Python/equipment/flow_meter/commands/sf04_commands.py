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
#------------------------------------------------------------#
# Note(s):                                                   #
# Codes adapted from                                         #
# - SHDLC_communicator.py                                    #
# - example_3_continuous_measurement_SF04.py                 #
# - example_4_continuous_measurement_SF06.py                 #
# provided by Sensirion support                              #
###========================================================###

from equipment.flow_meter.commands.shdlc_functions import send

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------------------------
# Set the resolution of the flowmeter to 16 bit
def set_resolution_sf04(board, debug=False):
    #send(board, 0, 0x41, [16], debug=debug)
    board.SHDLC_send_and_receive(0, 0x41, [16])

# ----------------------------------
# Toggle the heater of the flowmeter
def toggle_heater_sf04(board, status, debug=False):

    # Get the command to send
    if status:
        command = [1]
    else:
        command = [0]

    # Send the command to the flowmeter
    #send(board, 0, 0x42, command, debug=debug)
    board.SHDLC_send_and_receive(0, 0x42, command)

# ------------------
# Make a measurement
def get_measurement_sf04(board, scale_factor, debug=False):

    # Enable the measurement
    #send(board, 0, 0x31, [], debug=debug)
    board.SHDLC_send_and_receive(0, 0x31, [])

    # Initialise the data
    data = []

    # Loop until data is available and has been read
    while len(data)<2:
        #data = send(board, 0, 0x32, [], debug=debug)
        data = board.SHDLC_send_and_receive(0, 0x32, [])

    # Combine the two data bytes into one 16bit data value
    value_from_sensor = data[0]*256 + data[1]

    # Compute two's complement (handle negative numbers!)
    if value_from_sensor >= 2**15:  # 2**15 = 32768
        value_from_sensor = value_from_sensor-2**16

    # Apply the scale factor
    value_from_sensor = value_from_sensor / scale_factor

    return value_from_sensor
