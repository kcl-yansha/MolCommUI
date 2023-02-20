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

import numpy as np

from equipment.equipment_class import Equipment
from equipment.connection.arduino import start_connection, stop_connection
from equipment.syringe_pump.commands import readFromArduino, checkProgress, checkSyringeBoard, editSettings, runSyringe, stopSyringe, getAxisID
from equipment.syringe_pump.properties import getVolume, getSpeed, getAcceleration, speedToUlMin, uLminToSpeed

from multithreading.threads.arduino_comm import ArduinoThreadContainer

from settings.equipment.syringe_calibration import loadSyringeCalibrationConfig, getSyringeTypeList
from settings.equipment.gearbox_calibration import loadGearboxCalibrationConfig, getGearboxesList
from settings.equipment.pid_calibration import loadPIDCalibrationConfig

##-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS FOR A SINGLE PUMP
##-/-/-/-/-/-/-/-/-/-/-/-/

class SyringePump:
    def __init__(self, parent):

        self.parent = parent

        # General properties
        self.name = "Syringe"
        self.microsteps = 16
        self.stype = getSyringeTypeList()[0]
        self.unit = 'mL/s'
        self.geartype = getGearboxesList()[0]
        self.pid_controller = None

        self.equipment = None

        # Values
        self.gear_ratio = 1.

        self.set_speed = 0.
        self.set_speed_ulmin = 0.

        self.speed = 0.
        self.speed_ulmin = 0.
        self.speed_factor = 1.
        self.acceleration = 99999.

        # Synchronisation
        self.assigned_flowmeter = None
        self.sync_flowmeter = None
        self.is_updated = True

        # Update properties
        self.updateSyringeType()
        self.updateGearboxType()

    ##-\-\-\-\-\-\-\-\
    ## SYNCHRONISATION
    ##-/-/-/-/-/-/-/-/

    # -----------------------------------------
    # Assign a flowmeter to the current syringe
    def assignFlowmeter(self, flowmeter):

        # Assign the flowmeter to the syringe pump
        self.assigned_flowmeter = flowmeter
        self.sync_flowmeter = flowmeter

        flowmeter.assigned_pump = self
        flowmeter.sync_pump = self

    # ----------------------------
    # De-synchronise the flowmeter
    def desyncFlowmeter(self):

        # Remove the pump from the flowmeter
        self.sync_flowmeter.deleteSpeed(self)

        self.sync_flowmeter.assigned_pump = None
        self.sync_flowmeter.sync_pump = None

        # Assign the flowmeter to the syringe pump
        self.assigned_flowmeter = None
        self.sync_flowmeter = None

    # ----------------------------
    # Set the speed of the syringe
    def editSetSpeed(self, value):

        # Set the speed
        self.set_speed = value

        # Convert to the desired value
        self.set_speed_ulmin = speedToUlMin(value, self.unit)

        # Set the speed in the flowmeter
        if self.sync_flowmeter is not None and self.equipment.is_running:
            self.sync_flowmeter.addSpeed(self, value)

        # Set the current speed
        self.editSpeed(value)

    # -----------------------------
    # Edit the speed of the syringe
    def editSpeed(self, value):

        # Set the speed
        self.speed = value

        # Convert to the desired value
        self.speed_ulmin = speedToUlMin(value, self.unit)

    # ------------------------------
    # Get data from the syringe type
    def updateSyringeType(self):

        # Extract the syringe type
        syringe_properties = loadSyringeCalibrationConfig(self.stype)

        # Calculate the section area of the syringe
        section = np.pi * ( syringe_properties['diameter']/2 )**2

        # Apply the values
        self.volume = syringe_properties['volume']
        self.diameter = syringe_properties['diameter']
        self.calibration_factor = syringe_properties['calibration_factor']

        # Set volume infos
        self.set_volume = syringe_properties['volume'] * 1000
        self.set_volume_perc = 100
        self.set_volume_text = 'ALL'

        # Calculate the section area of the syringe
        self.area = np.pi * (syringe_properties['diameter']/2)**2 / self.calibration_factor # Divide by the factor to make calibration intuitive

    # ------------------------------
    # Get data from the gearbox type
    def updateGearboxType(self):

        # Extract the gearbox type
        gearbox_properties = loadGearboxCalibrationConfig(self.geartype)

        # Calculate the speed ratio
        self.gear_ratio = gearbox_properties['ratio'] * gearbox_properties['calibration_factor']

    ##-\-\-\-\-\-\-\-\-\-\
    ## SETTINGS MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Generate the config dictionary
    def getSettings(self):

        # Make the property dictionary
        config_dict = {
        # General
        'type':'syringe',
        'syringe':self.stype,
        'ratio':self.geartype,
        # Settings
        'speed':self.speed,
        'speed_unit':self.unit,
        'acceleration':self.acceleration
        }

        return config_dict

    # --------------------------
    # Load the config dictionary
    def loadSettings(self, config_dict):

        # Load the properties
        self.name = config_dict['name']
        self.stype = config_dict['syringe']
        self.geartype = config_dict['ratio']
        self.unit = config_dict['speed_unit']

        # Load the values
        self.speed = float( config_dict['speed'] )
        self.acceleration = float( config_dict['acceleration'] )

        # Update properties
        self.updateSyringeType()
        self.updateGearboxType()

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS FOR A GROUP OF PUMPS
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class SyringeGroup:
    def __init__(self, parent, board, port):

        # General properties
        self.parent = parent
        self.name = checkSyringeBoard( board ) # Retrieve the ID from the board
        self.board = board
        self.serial_port = port

        # Initiliase the pump selection
        self.syringes = {
        'X': None,
        'Y': None,
        'Z': None,
        'A': None
        }

        self.syringe_equipments = {
        'X': None,
        'Y': None,
        'Z': None,
        'A': None
        }

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # --------------------------------
    # Close the connecton to the group
    def close(self):

        # Interrupt the thread
        #self.thread.interrupt()
        pass

    # ---------------------------------
    # Close the connection to the board
    def _close_connection(self):
        stop_connection(self.board)

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
    def addSyringe(self, parent, axis='X'):
        self.syringes[axis] = SyringePump(parent)

    # -----------------------------------------
    # Remove the selected syringe from the list
    def removeSyringe(self, axis='X'):

        # Remove the current selection
        self.syringes[axis] = None
        self.syringe_equipments[axis] = None

        # Disconnect if everything is removed
        _delete = True
        for crt_axis in self.syringes.keys():
            if self.syringes[crt_axis] is not None:
                _delete = False

        if _delete:
            self.close()

        return _delete

    ##-\-\-\-\-\-\-\-\-\-\
    ## SETTINGS MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Generate the config dictionary
    def getSettings(self):

        # Get the initial dictionary
        config_dict = {
        'type':'group'
        }

        # Check all the syringes
        for axis in self.syringes.keys():

            if self.syringes[axis] is not None:
                config_dict[axis.lower()] = self.syringes[axis].getSettings()
                config_dict[axis.lower()]['name'] = self.syringes[axis].name

        return config_dict

    # --------------------------
    # Load the config dictionary
    def loadSettings(self, config_dict):

        # Apply the properties
        self.name = config_dict['name']

        # Apply changes for every syringes
        for axis in ['x','y','z','a']:
            if self.syringes[axis.upper()] is not None and axis in config_dict.keys():
                self.syringes[axis.upper()].loadSettings( config_dict[axis] )

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS TO DEFINE THE SYRINGE AS AN EQUIPMENT
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class SyringeEquipment(Equipment):
    def __init__(self, instance, axis_port='X', debug=False, verbose=True):

        # Intialise the equipment class
        Equipment.__init__(self, 'syringe_pump')
        self.is_running = False
        self.parent = instance.parent

        self.widget = None

        # Save the equipment
        self.equipment = instance.syringes[ axis_port ]
        self.name = self.equipment.name
        self.axis = axis_port
        self.syringe_group = instance
        self.id = self.syringe_group.serial_port.replace('/','') +'_'+ self.axis

        # Assign inside the equipment
        self.equipment.equipment = self
        self.syringe_group.syringe_equipments[ axis_port ] = self

        self.debug = debug
        self.verbose = verbose

        # Prepare for saving data
        self.file_name_set = "untitled_set"
        self.file_name_pid = "untitled_pid"
        self.header = {'comments':[], 'header':[]}

        self.initThread()

        self.getFileInfos()

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # ----------------------------
    # Get the name for file saving
    def getFileInfos(self):

        # Get the file name
        self.file_name_set = self.syringe_group.serial_port.replace('/','') + '_' + self.equipment.name.lower().replace(' ','') + '_set'
        self.file_name_pid = self.syringe_group.serial_port.replace('/','') + '_' + self.equipment.name.lower().replace(' ','') + '_pid'

        # Get the column names
        columns_set = ['Time (s)','Flowrate','Unit']
        columns_pid = ['Time (s)','Flowrate','Unit','Error (µL/min)','P','I','D']

        # Get the informations
        infos = [
        'Syringe: '+self.equipment.name+' ('+self.equipment.stype+')',
        'Port: '+str(self.syringe_group.serial_port)
        ]

        # Make the dictionary
        self.header_set = {'comments':infos, 'header':columns_set}
        self.header_pid = {'comments':infos, 'header':columns_pid}

    # ------------------
    # Remove the syringe
    def removeSyringe(self):
        return self.syringe_group.removeSyringe(self.axis)

    ##-\-\-\-\-\-\-\-\-\-\
    ## THREAD COMMUNICATION
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------------------
    # Initialise the flowmeter thread and add the flowmeter to it
    def initThread(self):

        # Initialise the thread
        if 'syringe_pump' not in self.parent.threads.keys():
            self.parent.threads['syringe_pump'] = ArduinoThreadContainer(self.parent)
        self.parent.threads['syringe_pump'].addEquipment(self)

    # ------------------------
    # Enqueue the next command
    def enqueue(self, id, event_type, fn, *args, **kwargs):
        self.parent.threads['syringe_pump'].enqueue( id, event_type, fn, *args, **kwargs )

    ##-\-\-\-\-\-\-\
    ## UPDATE METHODS
    ##-/-/-/-/-/-/-/

    # -----------------
    # Save the progress
    def _update_progress(self, value):

        try:
            value = float(value)

            # Update the status
            if value == 0:

                # Set the boolean
                self.equipment.is_running = False

                # Update bar colour if needed
                self.equipment.widget.updateRunning()

        except:
            pass

    ##-\-\-\-\-\
    ## UI UPDATE
    ##-/-/-/-/-/

    # -----------------------
    # Update the UI if needed
    def updateRunning(self):

        # Update the widget
        if self.widget is not None:
            self.widget.updateRunning()

    ##-\-\-\-\
    ## COMMANDS
    ##-/-/-/-/

    # ---------------------------------
    # Run the motor for the given value
    def run(self, volume=None):

        # Get default volume
        if volume is None:
            volume = 1000 # TO BE CHANGED

        # Calculate the displacement
        new_volume = getVolume( volume, self.equipment.unit, self.equipment.area, self.equipment.microsteps )

        # Correct the volume by the gear ratio
        new_volume *= self.equipment.gear_ratio

        # Get the pump parameters
        board = self.syringe_group.board

        # Run the command
        self.enqueue(self.id, self.id+'-run', runSyringe, self, board, new_volume, axis=self.axis, verbose=self.verbose)

        # Write the change in the experiment file
        value = np.array([self.equipment.speed, self.equipment.unit])
        self.equipment.parent.experiment.save(self.file_name_set, value, header=self.header_set)

        # Set the speed in the flowmeter
        if self.equipment.sync_flowmeter is not None:
            self.equipment.sync_flowmeter.addSpeed(self.equipment, self.equipment.set_speed_ulmin)
            self.equipment.sync_flowmeter.resetFeedback()

    # -------------------------------
    # Check the progress of the motor
    def check(self):

        # Run the command
        if self.is_running:

            # Send the new check command
            self.enqueue(self.id, self.id+'-check', checkProgress, self, self.syringe_group.board, axis=self.axis, verbose=self.verbose, is_unique=True)

    # --------------
    # Stop the motor
    def stop(self):

        # Run the command
        self.enqueue(self.id, self.id+'-stop', stopSyringe, self, self.syringe_group.board, axis=self.axis, verbose=self.verbose, priority=True, flush_equipment=True)

        # Write the change in the experiment file
        value = np.array([0., self.equipment.unit])
        self.equipment.parent.experiment.save(self.file_name_set, value, header=self.header_set)

        # Set the speed in the flowmeter
        if self.equipment.sync_flowmeter is not None:
            self.equipment.sync_flowmeter.deleteSpeed(self.equipment)
            self.equipment.sync_flowmeter.resetFeedback()

    # ------------------------------
    # Apply the speed to the syringe
    def setSpeed(self, pid_data=None, priority=False):

        # Calculate the speed
        new_speed = getSpeed( self.equipment.speed, self.equipment.unit, self.equipment.area, self.equipment.microsteps )
        new_speed *= self.equipment.gear_ratio

        # Get the pump parameters
        board = self.syringe_group.board

        # Run the command
        self.enqueue(self.id, self.id+'-settings', editSettings, self, new_speed, 'speed', axis=self.axis, verbose=self.verbose, priority=priority, make_unique=priority)

        # Write the change in the experiment file
        value = np.array([self.equipment.speed, self.equipment.unit])

        # Add information from the feedback control
        if pid_data is not None:
            value = np.concatenate([value, pid_data])

            self.equipment.parent.experiment.save(self.file_name_pid, value, header=self.header_pid)

        else:
            if self.equipment.sync_flowmeter is not None:
                self.equipment.sync_flowmeter.resetFeedback()

            self.equipment.parent.experiment.save(self.file_name_set, value, header=self.header_set)

        # Edit the interface (2)
        if 'pid_calibration' in self.parent.subWindows.keys():
            if self.parent.subWindows['pid_calibration'] is not None:
                self.parent.subWindows['pid_calibration'].updateInjection(self.equipment.speed_ulmin)

    # -------------------------------------
    # Apply the acceleration to the syringe
    def setAccel(self):

        # Calculate the acceleration
        #new_accel = getAcceleration( self.equipment.acceleration, self.equipment.unit, self.equipment.area, self.equipment.microsteps )
        new_accel = getAcceleration( self.equipment.acceleration, 'mL/s', self.equipment.area, self.equipment.microsteps )

        # Get the pump parameters
        board = self.syringe_group.board

        # Run the command
        self.enqueue(self.id, self.id+'-settings', editSettings, self, new_accel, 'accel', axis=self.axis, verbose=self.verbose)

        # Reset the feedback control memory
        if self.equipment.sync_flowmeter is not None:
            self.equipment.sync_flowmeter.resetFeedback()

##-\-\-\-\-\-\-\-\
## PRIVATE FUNCTION
##-/-/-/-/-/-/-/-/

# --------------------------
# Initialise a syringe group
def _gen_new_group(board, parent, port):

    # Create a new class
    new_class = SyringeGroup(parent, board, port)

    # Assign a syringe to each axis port
    for i, axis in enumerate(new_class.syringes.keys()):
        new_class.syringes[ axis ] = SyringePump(parent)
        new_class.syringes[ axis ].name += " " + str(i+1)

    return new_class

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

# -----------------------------------------
# Check the syringe group at the given port
def checkSyringeGroupPort(port, baudrate=9600): # 230400

    # Open the port to check it
    board = start_connection(port, baudrate)

    # Check the port
    checkSyringeBoard(board)

    # Close the port
    #stop_connection(board)

    return True

# ----------------------------------------
# Load the syringe group at the given port
def loadSyringeGroupClass(parent, port, baudrate=9600):

    # Open the port to check it
    board = start_connection(port, baudrate)

    # Check that the port opening was successful
    if board is not None:

        # Check the initial state
        board_answer = readFromArduino(board, timeout=3)

        # Proceed
        if board_answer is not None:

            # Create a new class
            syringe_class = _gen_new_group(board, parent, port)
            print(board.name + ': Received '+syringe_class.name)
            print('--------------------')

            return syringe_class

    # Return an empty class if nothing worked
    return None
