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

from user_interface.equipment_config.syringe_pump.arduino_group.display import setArduinoGroupWindow
from user_interface.equipment_config.flow_meter.display import setFlowMeterWindow
from user_interface.equipment_config.spectrometer.connection.display import setSpectroMeterWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class connectEquipmentFunctions(object):

    # --------------------------
    # Open the connection window
    def startConnectionMenu(self):

        # Get the selection from the combo box
        selection = self.combobox.currentText()

        # Select what to do
        if selection == 'Syringe Pump':
            openWindow(self.parent, setArduinoGroupWindow, 'arduino_group')

        elif selection == 'Flow Meter':
            openWindow(self.parent, setFlowMeterWindow, 'flow_meter')

        elif selection == 'Spectrometer':
            openWindow(self.parent, setSpectroMeterWindow, 'spectrometer')

        # Close the current one
        self.close()
