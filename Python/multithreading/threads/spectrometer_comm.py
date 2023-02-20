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
    result = qtc.pyqtSignal(object)
    progress = qtc.pyqtSignal(int)

##-\-\-\-\-\-\-\-\-\-\
## MAIN PROCESS THREAD
##-/-/-/-/-/-/-/-/-/-/

class SpectroMeterThread(qtc.QThread):

    def __init__(self, spectrometer): #, fn, *args, **kwargs):
        parent = None
        super(SpectroMeterThread, self).__init__(parent)

        # Define the main parameters
        self.spectrometer = spectrometer
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

            # Get the initial time
            start_time = time.time()

            # Process the next command in line if any
            state, equipment_id, active_output, verbose = self.queue.dequeue()
            if state and active_output is not None:

                # Send the feedback
                self.signals.result.emit(active_output)
                #self.flowmeter.getChange(active_output)

                # Wait until the delay time is over
                wait_time = 2*self.spectrometer.integration_time/1000 - (time.time() - start_time)
                if wait_time > 0:
                    time.sleep(wait_time)

            else:
                time.sleep(0.1)

        #if self.queue.getCount() > 0:
        #    self.run()

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
