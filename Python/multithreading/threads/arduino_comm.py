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

from equipment.syringe_pump.commands import readFromArduino

##-\-\-\-\-\-\
## SIGNAL CLASS
##-/-/-/-/-/-/

class WorkerSignals(qtc.QObject):

    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    result = qtc.pyqtSignal(tuple)
    progress = qtc.pyqtSignal(tuple)

##-\-\-\-\-\-\-\-\-\-\
## MAIN PROCESS THREAD
##-/-/-/-/-/-/-/-/-/-/

class ArduinoThread(qtc.QThread):

    def __init__(self): #, fn, *args, **kwargs):
        parent = None
        super(ArduinoThread, self).__init__(parent)

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
            state, pump_id, active_output, verbose = self.queue.dequeue()

            # Get the result of the active output
            if state and active_output is not None:

                # Display the output in the console
                if isinstance(active_output, str):
                    if verbose:
                        print(active_output)

                else:

                    # Read the multiple output
                    out_type, axis, value = active_output

                    # Process a check
                    if out_type == 'check':
                        self.signals.result.emit( (pump_id,value) )
                        #print('check for',axis,value)

            else:
                time.sleep(0.1)

        self.signals.finished.emit()
        self.stop()

    # ------------------------------------
    # Run the process in a separate thread
    def _old_run(self):

        """
        Original thread from the Poseidon code - keep it oonly for backup purposes
        """

        # Attempt to run the function
        try:
            result = self.fn(*self.args, **self.kwargs)

        # Raise an error if the thread cannot be started
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        # Return the result
        else:
            self.signals.result.emit(result)

        # Interrupt the job
        finally:
            self.signals.finished.emit()  # Done
            self.stop()

            print("Job completed")

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

class ArduinoThreadContainer:

    def __init__(self, parent):
        self.parent = parent

        # Initialise the equipment list
        self.equipments = {}

        # Initialise the thread
        self.thread = ArduinoThread()
        self.thread.signals.result.connect(self.getChange)
        self.thread.start()

    ##-\-\-\-\-\-\-\
    ## COMMUNICATION
    ##-/-/-/-/-/-/-/

    # ------------------------
    # Enqueue the next command
    def enqueue(self, equipment_id, event_type, fn, *args, **kwargs):
        self.thread.queue.enqueue( equipment_id, event_type, fn, *args, **kwargs )

    # ------------------------------------
    # Get the change from the syringe pump
    def getChange(self, output):
        id, value = output
        self.equipments[id]._update_progress(value)

    ##-\-\-\-\-\-\-\-\
    ## MANAGE EQUIPMENT
    ##-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Add the selected equipment to the list
    def addEquipment(self, pump):
        self.equipments[pump.id] = pump

    # -------------------------------------
    # Remove the selected key from the list
    def removeEquipment(self, pump_id):

        # Remove the key
        self.equipments.pop(pump_id, None)

        # Terminate the thread
        if len(self.equipments.keys()) == 0:
            print('Empty')
