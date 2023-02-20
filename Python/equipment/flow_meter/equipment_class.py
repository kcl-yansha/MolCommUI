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
import time

from equipment.connection.arduino import start_connection, stop_connection
from equipment.flow_meter.calculation import apply_filter, speed_correction
from equipment.flow_meter.commands import connect_flowmeter, get_ID, init_flowmeter, close_flowmeter, get_measurement
from equipment.flow_meter.properties import getFlowMeterType
from equipment.pid_controller import PIDController

from multithreading.threads.flowmeter_comm import FlowMeterThread, FlowMeterThreadContainer

from settings.equipment.pid_calibration import loadPIDCalibrationConfig

##-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS FOR A SINGLE PUMP
##-/-/-/-/-/-/-/-/-/-/-/-/

class FlowMeter:
    def __init__(self, parent, board, port, debug=True):

        # General properties
        self.name = "Flow Meter"
        self.ftype = 'SLI-0430'
        self.chip = 'SF04'
        self.serial_port = port
        self.board = board
        self.equipment_id = port
        self.serial_number = ''

        self.parent = parent
        self.widget = None
        self.assigned_pump = None
        self.sync_pump = None

        self.debug = debug
        self.delay = 100

        # Flow meter properties
        self.scale_factor = 270
        self.min_range = 1
        self.max_range = 120
        self.unit = 'µL/min'

        # Flow meter values
        self.is_running = False
        self.read_values = False
        self.last_value = 0

        # Feedback parameters
        self.feedback = PIDController()
        self.feedback.sensor = self
        self.pid_controller = None

        # Filter
        self.use_previous = False
        self.previous_values = []
        self.n_previous = 10

        # Main thread
        self.initThread()

        # Prepare for saving data
        self.file_name = "untitled"
        self.header = {'comments':[], 'header':[]}

        self.getFileInfos()

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # --------------------------------
    # Close the connecton to the group
    def close(self):

        # Close the connection
        self.terminate()

        # Interrupt the thread
        self.parent.threads['flowmeter'].removeEquipment(self.equipment_id)

    # ---------------------------------
    # Close the connection to the board
    def _close_connection(self):
        self.board.close()

    # ------------------------------
    # Get the header for file saving
    def getFileInfos(self):

        # Define the name of the file to save
        self.file_name = self.serial_port.replace('/','') + '_' + self.serial_number.lower().replace(' ','') + '_' + self.name.lower().replace(' ','')

        # Get the column names
        columns = ['Time (s)','Flowrate ('+self.unit+')']

        # Get the informations
        infos = [
        'Flowmeter: '+self.name+' ('+self.ftype+')',
        'Port: '+str(self.serial_port),
        'S/N: '+self.serial_number
        ]

        # Make the dictionary
        self.header = {'comments':infos, 'header':columns}

    ##-\-\-\-\-\-\-\-\-\-\
    ## THREAD COMMUNICATION
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------------------
    # Initialise the flowmeter thread and add the flowmeter to it
    def initThread(self):

        # Initialise the thread
        if 'flowmeter' not in self.parent.threads.keys():
            self.parent.threads['flowmeter'] = FlowMeterThreadContainer(self.parent)
        self.parent.threads['flowmeter'].addEquipment(self)

    # ------------------------
    # Enqueue the next command
    def enqueue(self, event_type, fn, *args, **kwargs):
        self.parent.threads['flowmeter'].enqueue( self.equipment_id, event_type, fn, *args, **kwargs )

    # ------------------------------
    # Get the change from the thread
    def getChange(self, value):
        if self.debug:
            print(self.name+':', value, self.unit)

        # Convert to float
        value = float(value)

        # Apply a filter
        if self.use_previous:
            value = apply_filter(value, self)

        # Save the last change
        self.last_value = [time.time(), value]

        # Check if the speed needs correction
        self.checkSpeed()

        # Do another measurement
        if self.read_values:
            self.read()

        # Write to file in the experiment
        self.parent.experiment.save(self.file_name, value, header=self.header)

        # Edit the interface (1)
        if self.widget is not None:
            self.widget.updateFlowRate(value)

        # Edit the interface (2)
        if 'pid_calibration' in self.parent.subWindows.keys():
            if self.parent.subWindows['pid_calibration'] is not None:
                self.parent.subWindows['pid_calibration'].updateFlowRate(self.last_value)

    ##-\-\-\-\
    ## COMMANDS
    ##-/-/-/-/

    # ----------------------------------
    # Toggle the heater of the flowmeter
    def init(self, ftype='SLI-0430'):

        # Save the type of flowmeter to use
        self.ftype = ftype

        # Get the properties
        properties = getFlowMeterType()
        properties = properties[ftype]

        # Apply the properties
        self.chip = properties['chip']
        self.scale_factor = properties['scale_factor']
        self.min_range = properties['min_range']
        self.max_range = properties['max_range']
        self.unit = properties['unit']

        # Initialise the flowmeter
        init_flowmeter(self.board, self.chip, debug=self.debug)

    # -----------------------------------
    # Set the resolution of the flowmeter
    def terminate(self):
        close_flowmeter(self.board, self.chip, debug=self.debug)

    # ------------------------
    # Read the flowmeter value
    def read(self):
        self.enqueue(self.equipment_id+'-read', get_measurement, self.board, self.chip, self.scale_factor, debug=self.debug, is_unique=True)

    ##-\-\-\-\-\-\-\-\
    ## FEEDBACK CONTROL
    ##-/-/-/-/-/-/-/-/

    # ---------------------
    # Set the PID constants
    def setPIDValues(self, pid_dict):
        self.feedback.setPIDvalues(pid_dict)

    # -------------------------------------
    # Get data from the PID controller type
    def updatePIDType(self):

        if self.pid_controller is not None:
            self.feedback.updateType(self.pid_controller)

    # ------------------------------
    # Reset the feedback loop memory
    def resetFeedback(self):

        self.feedback.resetMemory()

    # -------------------------
    # Add the speed to the list
    def addSpeed(self, pump, speed):

        # Add the pump to the list
        self.feedback.addSpeed(pump, speed)

        # Compute the new full speed
        return self.feedback.getFullSpeed()

    # ------------------------------
    # Remove the speed from the list
    def deleteSpeed(self, pump):

        # Remove the pump from the dictionary
        self.feedback.deleteSpeed(pump)

        # Compute the new full speed
        return self.feedback.getFullSpeed()

    # ----------------------
    # Compute the full speed
    def getFullSpeed(self):
        self.full_speed = np.sum( [self.all_speeds[x] for x in self.all_speeds.keys()] )

        return self.full_speed

    # -------------------------------------
    # Check and correct the speed if needed
    def checkSpeed(self):
        self.feedback.getCorrection()

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Load the flow meter at the given port
def loadFlowMeterClass(parent, port, baudrate=115200, debug=False):

    # Open the port to check it
    print(port)
    board = connect_flowmeter(port)

    # Check that the port opening was successful
    if board is not None:
        print('Connected to Flow meter')
        print('--------------------')

        # Initialise the class
        new_class = FlowMeter(parent, board, port, debug=debug)

        try:

            # Get the ID of the serial number
            new_class.serial_number = str( get_ID(board) )

            return new_class

        # Raise an error if the commands cannot be sent
        except:

            # Stop the connection to the board
            stop_connection(board)

            return None

    # Return an empty class if nothing worked
    return None
