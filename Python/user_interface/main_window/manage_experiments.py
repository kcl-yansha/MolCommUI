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

from input_output.experiments.experiment_class import copyExperiment

##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUIExperimentFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## EXPERIMENTS MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Toggle the status of the recording
    def toggleRecording(self, status):

        self.experiment.recording = status
        self.experimentDisplay.setExperimentStatus(self.experiment.recording)

    # ------------------------
    # Duplicate the experiment
    def duplicateExperiment(self):

        # Make the copy
        new_experiment = copyExperiment(self, self.experiment)

        # Apply the copy
        self.experiment = new_experiment
        self.experimentDisplay.setExperimentName(new_experiment.name)
        self.experimentDisplay.setExperimentStatus(new_experiment.recording)
