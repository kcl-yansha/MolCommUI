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

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw


##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class experimentDisplayFunctions(object):

    ##-\-\-\-\-\-\-\
    ## UPDATE THE UI
    ##-/-/-/-/-/-/-/

    # ---------------------------
    # Set the new experiment Name
    def setExperimentName(self, name):

        text = 'Experiment: '+name.strip()
        self.experimentName.setText(text)

    # -------------------------
    # Set the experiment status
    def setExperimentStatus(self, status):

        text = 'Status: '
        if status:
            text += 'Recording'
        else:
            text += 'Idle'

        self.experimentStatus.setText(text)
