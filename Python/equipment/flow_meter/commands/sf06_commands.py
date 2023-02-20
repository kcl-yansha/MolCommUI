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

from equipment.flow_meter.commands.shdlc_functions import send

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------
# Make a measurement
def get_measurement_sf06(board, scale_factor, debug=False):

    # Enable the measurement
    MEASUREMENT_TIME = 20 # set to 20 ms
    board.SHDLC_send_and_receive(0,0x33,
                                    [(MEASUREMENT_TIME & 0xFF00) >> 8, MEASUREMENT_TIME & 0xFF,
                                     0x36,0x08])
    board.SHDLC_send_and_receive(0,0x33,[])

    # Initialise the data
    data = []

    # Loop until data is available and has been read
    while len(data)<2:
        data = board.SHDLC_send_and_receive(0,0x36,[0x03])

    # Unpack the returned array
    packageslostcount = data[0]*0x1000000 + data[1]*0x10000 + data[2]*0x100 + data[3]
    packagesremainingcount = data[4]*0x100 + data[5]
    interlaceddatacount = data[6]*0x100 + data[7]
    measurements = data[8:]

    # Sort out the byte pairs of flow, temp and scale factor
    flowbytes = [m for e,m in enumerate(measurements) if e%6 == 0 or e%6 == 1]

    # Combine the byte pairs for i16t values
    flows = []
    for e,s in enumerate(flowbytes):
        if e%2 == 0:
            flows.append(s << 8)
        else:
            flows[-1] = flows[-1] + s

    # Two's complement
    flows = [f if f < 32768 else f - 65536 for f in flows]

    # Scale
    flows = [float(f)/scale_factor for f in flows]

    return flows[-1] # Only keep the last value

# ------------------------------------
# Reset the connection to a SCC1 cable
def reset_cable_sf06(board, debug=False):
    board.SHDLC_send_and_receive(0, 0xD3, [])
    time.sleep(0.100)

# ---------------
# Set sensor type
def set_sensor_sf06(board, debug=False):

    ## SET SENSOR TYPE
    board.SHDLC_send_and_receive(0, 0x24, [3])

    ## RESET SENSOR TYPE
    board.SHDLC_send_and_receive(0, 0x65, [])

    board.SHDLC_send_and_receive(0, 0x50, [])
