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

from equipment.spectrometer.equipment_class import loadSpectroMeterClass

from user_interface._common_functions.path_to_assets import getIcon
from user_interface.popups.notifications import warningProceedMessage, errorMessage

from settings.equipment.reload_equipment import addPort

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class editSpectroMeterFunctions(object):

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # --------------------------------------
    # Save the details in a new spectrometer
    def saveSpectroMeter(self):

        # Save the current settings
        self.spectrometer.name = self.spectroMeterName.text()
        self.spectrometer.setIntegrationTime( self.integrationSpinBox.value() )
        self.spectrometer.delay_time = self.delaySpinBox.value()

        self.close()
