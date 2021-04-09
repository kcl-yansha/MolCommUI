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
