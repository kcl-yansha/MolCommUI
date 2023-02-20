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

from user_interface._common_functions.window_handling import openWindow
from user_interface.popups.notifications import errorMessage, warningProceedMessage
from user_interface.popups.pump_synchronisation.display import synchroniseSyringeWindow
from user_interface.equipment_config.flow_meter.display import setFlowMeterWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class FlowMeterGroupFunctions(object):

    ##-\-\-\-\-\-\
    ## CONTROL PUMP
    ##-/-/-/-/-/-/

    # --------------------------------------
    # Send the read command to the flowmeter
    def sendReadCommand(self, direction=1):

        # Change the status
        self.flowmeter.is_running = True
        self.flowmeter.read_values = True

        # Send the command
        self.flowmeter.read()

    # --------------------------------
    # Send the stop command to the pump
    def sendStopCommand(self):
        self.flowmeter.is_running = False
        self.flowmeter.read_values = False

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # ------------------------------------
    # Define the range of the progress bar
    def setBarRange(self):
        self.capacityProgressBar.setMinimum(0)
        self.capacityProgressBar.setMaximum( int(self.flowmeter.max_range) )

    # --------------------
    # Update the flow rate
    def updateFlowRate(self, value):

        # Update the text display
        text_value = "{:.2f}".format(round(value, 2))
        self.speedDisplay.setText( text_value )

        # Update the progress bar display
        self.capacityProgressBar.setValue( int(value) )

    # -------------------------
    # Display the flowrate unit
    def displayUnit(self):
        self.speedLabel.setText( self.flowmeter.unit )

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## GENERATE CONTEXT MENU
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Display the menu on a right click
    def showRightClickMenu(self, event):

        # Initialise the menu
        self.menu = qtw.QMenu()

        # Rename the group
        rename_action = self.menu.addAction("Rename flowmeter")
        rename_action.triggered.connect(self.renameItem)

        # Delete the group
        delete_action = self.menu.addAction("Delete flowmeter")
        delete_action.triggered.connect(self.deleteItem)

        # Display the menu at the mouse location
        action = self.menu.exec_(self.mapToGlobal(event))

    # ---------------
    # Rename the item
    def deleteItem(self):

        # Prompt the user
        ok = warningProceedMessage('Delete Flowmeter', 'Are you sure you want to disconnect and delete the selected flowmeter?')

        if ok:
            self.parent.groupDisplay.deleteFlowMeter(self)

    # ----------------
    # Rename the group
    def renameItem(self):

        # Prompt the user
        text, ok = qtw.QInputDialog.getText(self, 'Rename Flowmeter', 'Name:', text=self.flowmeter.name)

        # Apply the change
        if ok:
            self.flowmeter.name = text
            self.parent.groupDisplay.refreshUI()

    ##-\-\-\-\
    ## ACTIONS
    ##-/-/-/-/

    # --------------------------------
    # Open the settings of the syringe
    def openSettings(self):
        openWindow(self.parent, setFlowMeterWindow, 'flow_meter', flowmeter=self.flowmeter)
