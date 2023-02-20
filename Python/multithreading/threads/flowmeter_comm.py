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

import sys
import time
import traceback

import PyQt5.QtCore as qtc

from multithreading.queues import Queue

##-\-\-\-\-\-\
## SIGNAL CLASS
##-/-/-/-/-/-/

class WorkerSignals(qtc.QObject):

    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    result = qtc.pyqtSignal(tuple)
    progress = qtc.pyqtSignal(int)

##-\-\-\-\-\-\-\-\-\-\
## MAIN PROCESS THREAD
##-/-/-/-/-/-/-/-/-/-/

class FlowMeterThread(qtc.QThread):

    def __init__(self): #, fn, *args, **kwargs):
        parent = None
        super(FlowMeterThread, self).__init__(parent)

        # Define the main parameters
        self.queue = Queue()

        # Define the main parameters
        self.runs = True
        self.running = True

        # Assign the signals
        self.signals = WorkerSignals()

    # --------------------------------------
    # Process the queue in a separate thread
    def run(self):

        while self.running:

            # Process the next command in line if any
            state, equipment_id, active_output, verbose = self.queue.dequeue()
            if state and active_output is not None:

                # Send the feedback
                self.signals.result.emit((equipment_id, active_output))

            else:
                time.sleep(0.1)

        self.signals.finished.emit()
        self.stop()

    # ------------------
    # Interrupt the loop
    def interrupt(self):
        self.running = False

    # ---------------------
    # Interrupt the process
    def stop(self):
        self.runs = False

##-\-\-\-\-\-\-\-\
## THREAD CONTAINER
##-/-/-/-/-/-/-/-/

class FlowMeterThreadContainer:

    def __init__(self, parent):
        self.parent = parent

        # Initialise the equipment list
        self.equipments = {}

        # Initialise the thread
        self.thread = FlowMeterThread()
        self.thread.signals.result.connect(self.getChange)
        self.thread.start()

    ##-\-\-\-\-\-\-\
    ## COMMUNICATION
    ##-/-/-/-/-/-/-/

    # ------------------------
    # Enqueue the next command
    def enqueue(self, equipment_id, event_type, fn, *args, **kwargs):
        self.thread.queue.enqueue( equipment_id, event_type, fn, *args, **kwargs )

    # ---------------------------------
    # Get the change from the flowmeter
    def getChange(self, output):
        id, value = output
        self.equipments[id].getChange(value)

    ##-\-\-\-\-\-\-\-\
    ## MANAGE EQUIPMENT
    ##-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Add the selected equipment to the list
    def addEquipment(self, flowmeter):
        self.equipments[flowmeter.equipment_id] = flowmeter

    # -------------------------------------
    # Remove the selected key from the list
    def removeEquipment(self, flowmeter_id):

        # Remove the key
        self.equipments.pop(flowmeter_id, None)

        # Terminate the thread
        if len(self.equipments.keys()) == 0:
            print('Empty')
