##-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS FOR A SINGLE PUMP
##-/-/-/-/-/-/-/-/-/-/-/-/

class SyringePump:
    def __init__(self):

        # General properties
        self.name = "Syringe"
        self.stype = 'BD 1 mL'
        self.unit = 'mm/s'
        self.jog = '0.01'

        # Values
        self.speed = 0.
        self.acceleration = 0.

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS FOR A GROUP OF PUMPS
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class SyringeGroup:
    def __init__(self, port):

        # General properties
        self.name = 'Untitled group 1'
        self.serial_port = port

        # Initiliase the pump selection
        self.syringes = {
        'X': None,
        'Y': None,
        'Z': None
        }

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Get the list of active axis ports
    def getPorts(self, empty=False):

        # Get the list of names
        port_list = list( self.syringes.keys() )

        # Refine the list to exclude empty axis
        if empty:
            port_list = [x for x in port_list if self.syringes[x] is None]
        else:
            port_list = [x for x in port_list if self.syringes[x] is not None]

        return port_list

    # -----------------------------------
    # Add a new syringe on the given axis
    def addSyringe(self, axis='X'):
        self.syringes[axis] = SyringePump()

##-\-\-\-\-\-\-\-\
## PRIVATE FUNCTION
##-/-/-/-/-/-/-/-/

# --------------------------
# Initialise a syringe group
def _gen_new_group(port):

    # Create a new class
    new_class = SyringeGroup(port)

    # Assign a syringe to each axis port
    for i, axis in enumerate(new_class.syringes.keys()):
        new_class.syringes[ axis ] = SyringePump()
        new_class.syringes[ axis ].name += " " + str(i+1)

    return new_class

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

# ----------------------------------------
# Load the syringe group at the given port
def loadSyringeGroupClass(port):

    # Create a new class
    syringe_class = _gen_new_group(port)

    return syringe_class
