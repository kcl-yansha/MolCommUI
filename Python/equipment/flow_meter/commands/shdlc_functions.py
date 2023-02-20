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

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------
# Compute the checksum of a list of bytes
def _compute_SHDLC_checksum(listofbytes):

    # sum up all bytes
    tmpchecksum = sum(listofbytes)

    # take least significant byte
    tmpchecksum = tmpchecksum & 0xff

    # invert (bit-wise XOR with 0xff)
    tmpchecksum = 0xff ^ tmpchecksum

    return tmpchecksum

# --------------------------------------
# Perform byte stuffing on 'listofbytes'
def _byte_stuff(listofbytes):

        """
        i.e. replace special characters as follows:
        0x7e --> 0x7d, 0x5e
        0x7d --> 0x7d, 0x5d
        0x11 --> 0x7d, 0x31
        0x13 --> 0x7d, 0x33
        """

        # Start the loop
        i=0
        while i<len(listofbytes):
            if listofbytes[i]==0x7e:
                listofbytes[i]=0x7d
                listofbytes.insert(i+1,0x5e)
                i+=1
            elif listofbytes[i]==0x7d:
                listofbytes[i]=0x7d
                listofbytes.insert(i+1,0x5d)
                i+=1
            elif listofbytes[i]==0x11:
                listofbytes[i]=0x7d
                listofbytes.insert(i+1,0x31)
                i+=1
            elif listofbytes[i]==0x13:
                listofbytes[i]=0x7d
                listofbytes.insert(i+1,0x33)
                i+=1
            i+=1

        return listofbytes

# -------------------------------------------------------------------------
# Sends command 'commandID' with data 'data' to device on address 'address'
def _send_command(ser, address, commandID, data, debug=False):

    """
    address: number between 0 and 254 (address 255 is reserved for broad-cast)
    commandID: byte
    data: list of bytes
    """

    datalength = len(data)

    # compose command
    command = [address, commandID, datalength] + data
    if debug: print('command before checksum:',command)

    # compute checksum
    command.append(_compute_SHDLC_checksum(command))
    if debug: print('command with checksum:',command)

    # do byte stuffing
    command = _byte_stuff(command)
    if debug: print('command with byte stuffing:', command)

    # add start byte and stop byte
    command = [0x7e] + command + [0x7e]
    if debug: print('command with start stop byte:',command)

    # convert list of numbers to bytearray
    command = bytearray(command)

    # send command to the device
    ser.write(command)

# ------------------------------------------------------------------------------
# Reads the response from the SHDLC device and returns the data as list of bytes
def _get_response(ser, debug=False):

    response = []
    res = ''

    # Iterate read until res is empty or stop byte received
    firstbyte=True
    while True:
        res = ser.read(1)
        if not res:
            break
        elif firstbyte or (ord(res) != 0x7e):
            firstbyte = False
            response.append(ord(res))
        else:
            response.append(ord(res))
            break

    # print response as it comes from the device
    if debug: print('response from sensor:',response)

    # remove first element (the start byte) from the response
    response.pop(0)
    # remove the last element (the stop byte) form the response
    response.pop(-1)

    # print response without start- and stop-bytes
    if debug: print('response w/o start/stop:',response)


    # Check for bytes that are stuffed
    i = 0
    #loop through response list
    while i < len(response):
        if response[i] == 0x7D:
            # 0x7d marks stuffed bytes. see SHDLC documentation
            if response[i+1] == 0x5E:
                response[i] = 0x7E
            elif response[i+1] == 0x5D:
                response[i] = 0x7D
            elif response[i+1] == 0x31:
                response[i] = 0x11
            elif response[i+1] == 0x33:
                response[i] = 0x13
            response.pop(i+1)
        i+=1

    if debug: print('response w/o byte stuffing:',response)

    # confirm check sum is correct

    #remove last element from response-list and store it in variable checksum
    checksum = response.pop(-1)

    # compare to received checksum
    if debug: print('checksum correct?',checksum == _compute_SHDLC_checksum(response))

    if debug: print('response without checksum', response)
    if debug: print('address:',response[0])
    if debug: print('command:',hex(response[1]))
    if debug: print('status:', response[2])
    if debug: print('data length:', response[3])
    if debug: print('data:', response[4:])

    # return only the 'data' portion of the response
    return response[4:]

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------
# Communicate with the flowmeter board
def send(ser, address, commandID, data, debug=False):

    # Send the command
    _send_command(ser, address, commandID, data, debug=debug)

    # Wait for the answer
    response = _get_response(ser, debug=debug)

    return response
