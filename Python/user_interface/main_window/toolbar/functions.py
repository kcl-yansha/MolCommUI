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

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.connect_equipment.display import connectEquipmentWindow
from user_interface.popups.experiment_config.display import setExperimentWindow

from user_interface.scheduler.main_scheduler.display import setSchedulerWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class toolBarFunctions(object):

    # --------------------------
    # Open the connection window
    def callEquipmentConnectionWindow(self):
        openWindow(self.parent, connectEquipmentWindow, 'connect_equipment')

    # ------------------------------
    # Open the new experiment window
    def callNewExperimentWindow(self):
        openWindow(self.parent, setExperimentWindow, 'experiment')

    # ---------------------------
    # Copy the current experiment
    def copyCurrentExperiment(self):
        self.parent.duplicateExperiment()

    # ------------------------------
    # Start recording the experiment
    def startRecordingExperiment(self):
        self.parent.toggleRecording(True)

    # -----------------------------
    # Stop recording the experiment
    def stopRecordingExperiment(self):
        self.parent.toggleRecording(False)

    # -------------------------
    # Open the scheduler window
    def callSchedulerWindow(self):
        openWindow(self.parent, setSchedulerWindow, 'set_scheduler')
