###========================================================###
### MolCommUI --- v1.0                                     ###
### Date: 20/02/2023                                       ###
###========================================================###
# Codes adapted from the SHDLC_communicator.py code          #
# provided by Sensirion support for communication            #
# with Sensirion flowmeters                                  #
###========================================================###

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

class SHDLC_SerialConnection(object):
    """
    class to demonstrate SHDLC communication with RS485 adapter cable.

    (1) usage in normal mode:
    >>> sc=SHDLC_SerialConnection()
    >>> sc.open_connection(5)
    >>> ans=sc.SHDLC_send(0,0x41, [14])
    >>> ans
    ([],0)
    >>> ans=sc.SHDLC_send(0,0x41, [])
    >>> ans
    ([14],0)
    >>> sc.close()

    (2) usage in debug mode: (with additional information printed to STDOUT)
    >>> sc=SHDLC_SerialConnection(print_debug_info=True)
    >>> sc.open_connection(5)
    >>> ans=sc.SHDLC_send(0,0x41, [14])
    ################################################################
    sending command: 0x41
    to address:      0x0   (decimal: 0)
    with parameters: ['0xe']
    ----------------------------------------------------------------

    command before byte-stuffing and without start/stop bytes: ['0x0', '0x41', '0x1', '0xe', '0xaf']
    command sent: ['0x7e', '0x0', '0x41', '0x1', '0xe', '0xaf', '0x7e']

    response received: ['0x7e', '0x0', '0x41', '0x0', '0x0', '0xbe', '0x7e']
    response after byte-un-stuffing and without start/stop bytes: ['0x0', '0x41', '0x0', '0x0', '0xbe']

    return checksum OK?   : True
    response from address :0x0   (decimal: 0)
    response command      :0x41
    response error code   :0x0
    ################################################################

    >>> ans
    ([],0)
    >>> ans=sc.SHDLC_send(0,0x41, [])
    ################################################################
    sending command: 0x41
    to address:      0x0   (decimal: 0)
    with parameters: []
    ----------------------------------------------------------------

    command before byte-stuffing and without start/stop bytes: ['0x0', '0x41', '0x0', '0xbe']
    command sent: ['0x7e', '0x0', '0x41', '0x0', '0xbe', '0x7e']

    response received: ['0x7e', '0x0', '0x41', '0x0', '0x1', '0xe', '0xaf', '0x7e']
    response after byte-un-stuffing and without start/stop bytes: ['0x0', '0x41', '0x0', '0x1', '0xe', '0xaf']

    return checksum OK?   : True
    response from address :0x0   (decimal: 0)
    response command      :0x41
    response error code   :0x0
    ################################################################

    >>> ans
    ([14],0)
    >>> sc.close()
    """

    def __init__(self, print_debug_info=False):
        """
        Constructor. Initializes the serial connection to 'None'
        """
        self.conn=None
        self.debuginfo=print_debug_info

    def open_connection(self, port_id):
        """
        Open a serial connection on COM'windows_port_number' with the correct
        settings for the RS485-adapter-cable.
        Number for windows port! Str for unix port path!
        """

        # The port format depends on the hardware settings
        if type(port_id) == type(3):
            # Hand a number for a windows port
            port_number = "COM" + str(port_id)
        elif type(port_id) == type(""):
            # a unit path might look like this: '/dev/ttyUSB0'
            port_number = port_id
        else:
            raise TypeError("The COM port needs to be specified as number (Windows) or as a str of the path for unix!",
                            "Received type: " + str(type(port_id)))

        # Open Serial Port (for example USB to RS485 Adapter
        ser = serial.Serial(
            port = port_number,         #number of device, numbering starts at
                                        #zero.
            baudrate=115200,            #baudrate
            bytesize=serial.EIGHTBITS,  #number of databits
            parity=serial.PARITY_NONE,  #enable parity checking
            stopbits=serial.STOPBITS_ONE,  #number of stopbits
            timeout=1,                  #set a timeout value (example only because reset
                                        #takes longer)
            xonxoff=0,                  #disable software flow control
            rtscts=0,                   #disable RTS/CTS flow control
        )
        self.conn = ser

    def close(self):
        """
        Close the serial connection (and release the COM-port)
        """
        self.conn.close()

    def compute_checksum(self, listofbytes):
        """
        Compute the SHDLC check sum of 'listofbytes', where 'listofbytes' is a
        list of integers between 0 and 255, i.e. a byte array.
        """
        # sum up bytes
        chk = sum(listofbytes)
        # get least significant byte (take AND with 0xff)
        chk = chk & 0xff
        # invert (take XOR with 0xff)
        chk=0xff^chk
        return chk

    def byte_stuff(self, listofbytes):
        """
        Perform byte stuffing on 'listofbytes',
        i.e. replace special characters as follows:
        0x7e --> 0x7d, 0x5e
        0x7d --> 0x7d, 0x5d
        0x11 --> 0x7d, 0x31
        0x13 --> 0x7d, 0x33
        """
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

    def byte_unstuff(self, listofbytes):
        """
        Perform byte un-stuffing on 'listofbytes',
        i.e. substitute special characters back:
        0x7d, 0x5e --> 0x7e
        0x7d, 0x5d --> 0x7d
        0x7d, 0x31 --> 0x11
        0x7d, 0x33 --> 0x13
        """
        i=0
        while i<len(listofbytes):
            if listofbytes[i] == 0x7D:
                if listofbytes[i+1] == 0x5E:
                    listofbytes[i] = 0x7E
                elif listofbytes[i+1] == 0x5D:
                    listofbytes[i] = 0x7D
                elif listofbytes[i+1] == 0x31:
                    listofbytes[i] = 0x11
                elif listofbytes[i+1] == 0x33:
                    listofbytes[i] = 0x13
                listofbytes.pop(i+1)
            i+=1
        return listofbytes

    def SHDLC_send_and_receive(self, address, command, parameters):
        """
        address as integer
        command as integer
        send command to address using parameters.
        checksum computation and byte stuffing are done automatically.
        parameters: list of bytes (integers between 0 and 255)
        returns the reply form the sensor cable as tuple (data,error)
        where 'data' is a list of bytes and 'error' the error code
        """
        if self.debuginfo:
            print('  ------------------------------------')
            print('   sending command: ' + str(hex(command)))
            print('   to address:      ' + str(hex(address)) + "   (decimal: "+ str(address)+")")
            print('   with parameters: ' + str([str(hex(a)) for a in parameters]))
            print('   ------------------')
            print()

        # compose cmdarray
        cmdarray = bytearray([address, command, len(parameters)]+parameters)
        # insert checksum
        cmdarray.append(self.compute_checksum(cmdarray))

        if self.debuginfo:
            print('   command before byte-stuffing and without start/stop bytes: ' + str([str(hex(a)) for a in cmdarray]))

        # byte stuffing
        cmdarray = self.byte_stuff(cmdarray)
        # start byte
        cmdarray.insert(0, 0x7e)
        # stop byte
        cmdarray.append(0x7e)
        # write command string to serial port
        self.conn.write(cmdarray)
        if self.debuginfo:
            print('   byte sequence sent: ' + str([str(hex(a)) for a in cmdarray]))
            print()


        response = []
        res = True

        # Iterate read until res is empty == False
        is_first_byte=True
        while True:
            res = self.conn.read(1)
            if not is_first_byte and ord(res)==0x7e:
                response.append(ord(res))
                break
            is_first_byte=False
            if res:
                response.append(ord(res))
            else:
                break

        if self.debuginfo:
            print('   byte sequence received: ' + str([str(hex(a)) for a in response]))

        response.pop(0)
        response.pop(-1)
        response = self.byte_unstuff(response)

        if self.debuginfo:
            print('   response after byte-un-stuffing and without start/stop bytes: ' + str([str(hex(a)) for a in response]))
            print()
            print('   return checksum OK?   :' +str(response[-1]==self.compute_checksum(response[:-1])))
            print('   response from address :' + str(hex(response[0])) + "   (decimal: "+ str(response[0])+")")
            print('   response command      :' + str(hex(response[1])))
            print('   response error code   :' + str(hex(response[2])))
            print('   response data length  :' + str(hex(response[3])) + "   (decimal: "+ str(response[3])+")")
            print('   response data content :' + str([str(hex(a)) for a in response[4:-1]]))
            print('  ------------------------------------')
            print()

        return response[4:-1]#,response[2]
