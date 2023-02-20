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

import time

from equipment.connection.shdlc import SHDLC_SerialConnection
from equipment.flow_meter.commands.sf04_commands import get_measurement_sf04, set_resolution_sf04, toggle_heater_sf04
from equipment.flow_meter.commands.sf06_commands import get_measurement_sf06, reset_cable_sf06, set_sensor_sf06

"""
Codes adapted from
- SHDLC_communicator.py
- example_3_continuous_measurement_SF04.py
- example_4_continuous_measurement_SF06.py
provided by Sensirion support
"""

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------
# Connect to the flowmeter
def connect_flowmeter(port_id):

    # Initialise the serial connection and open the port
    sc = SHDLC_SerialConnection()
    sc.open_connection(port_id=port_id)

    return sc

# ------------------------
# Initialise the flowmeter
def init_flowmeter(board, chip='SF04', debug=False):

    # Initialise a SF04 flowmeter
    if chip == 'SF04':

        # Toggle the heater on
        toggle_heater_sf04(board, True, debug=debug)

        # Set the resolution of the flowmeter
        set_resolution_sf04(board, debug=debug)

    # Initialise a SF06 flowmeter
    elif chip == 'SF06':

        # Reset the connection to the cable
        reset_cable_sf06(board, debug=debug)

        # Set the type of sensor
        set_sensor_sf06(board, debug=debug)

# -------------------
# Close the flowmeter
def close_flowmeter(board, chip='SF04', debug=False):

    # Terminate a SF04 flowmeter
    if chip == 'SF04':

        # Toggle the heater off
        toggle_heater_sf04(board, False, debug=debug)

    # Terminate a SF06 flowmeter
    elif chip == 'SF06':

        """Do nothing"""

    # Close the connection
    board.close()

# --------------------
# Get the flowmeter ID
def get_ID(board, debug=False):

    # Retrieve the ID of the flowmeter
    data = board.SHDLC_send_and_receive(0,0x54,[])

    # Convert the output into a Serial Number u32 integer
    board_sn = int.from_bytes(data, byteorder='big', signed=False)

    return board_sn

# ------------------
# Make a measurement
def get_measurement(board, chip, scale_factor, debug=False):

    # Get measurement from a SF04 chip
    if chip == 'SF04':
        value = get_measurement_sf04(board, scale_factor, debug=debug)

    # Get measurement from a SF04 chip
    elif chip == 'SF06':
        value = get_measurement_sf06(board, scale_factor, debug=debug)

    return value
