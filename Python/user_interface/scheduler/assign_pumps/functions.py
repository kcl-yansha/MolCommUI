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

from multithreading.scheduler.events import Pulse

from user_interface._custom_widgets.comboboxes import AdvComboBox

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class assignPumpFunctions(object):

    ##-\-\-\-\-\-\-\
    ## INIT INTERFACE
    ##-/-/-/-/-/-/-/

    # ---------------------------------------
    # Populate the display with all the pumps
    def populatePumpList(self):

        # Process all the books
        self.pumpComboBoxes = []
        self.available_pumps = self.parent.equipments['syringe_pumps']
        self.available_pumps_name = [x.name for x in self.available_pumps]

        for pump in self.pump_names:

            # Make the widget
            pumpComboBox = AdvComboBox()
            pumpComboBox.addItems(self.available_pumps_name)

            # Add to the interface
            self.pumpComboBoxes.append([pumpComboBox, pump])
            self.pumpSelectionLayout.addRow( pump,  pumpComboBox )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------
    # Edit the settings of the pulse
    def setPulse(self):

        # Retrieve all the values
        pump_dict = {}
        for cbox, pump_name in self.pumpComboBoxes:

            crt_id = cbox.currentIndex()
            pump_dict[pump_name] = self.available_pumps[crt_id]

        # Assign the dict
        self.pump_dict = pump_dict

        # Refresh the display
        self.close()

    # ----------------
    # Return the value
    def GetValue(self):
        return self.pump_dict
