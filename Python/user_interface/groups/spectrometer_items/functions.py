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
from user_interface.equipment_config.spectrometer.edit.display import editSpectroMeterWindow

from user_interface.dock_window.spectrum_window.display import SpectrumDisplayPanel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class SpectroMeterGroupFunctions(object):

    ##-\-\-\-\-\-\
    ## CONTROL PUMP
    ##-/-/-/-/-/-/

    # -----------------------------------------
    # Send the read command to the spectrometer
    def sendReadCommand(self, direction=1):

        # Change the status
        self.spectrometer.is_running = True
        self.spectrometer.read_values = True

        # Send the command
        self.spectrometer.read()

    # --------------------------------
    # Send the stop command to the pump
    def sendStopCommand(self):
        self.spectrometer.is_running = False
        self.spectrometer.read_values = False

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # -----------------------------
    # Display the spectrometer unit
    def updateStatus(self):

        # Set the text
        if self.spectrometer.read_values:
            text = "> SCANNING <"
        else:
            text = "< Not scanning >"

        # Update the text
        self.statusDisplay.setText( text )

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## GENERATE CONTEXT MENU
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Display the menu on a right click
    def showRightClickMenu(self, event):

        # Initialise the menu
        self.menu = qtw.QMenu()

        # Delete the group
        delete_action = self.menu.addAction("Delete spectrometer")
        delete_action.triggered.connect(self.deleteItem)

        # Display the menu at the mouse location
        action = self.menu.exec_(self.mapToGlobal(event))

    # ---------------
    # Rename the item
    def deleteItem(self):

        # Prompt the user
        ok = warningProceedMessage('Delete Spectrometer', 'Are you sure you want to disconnect and delete the selected spectrometer?')

        if ok:
            self.parent.groupDisplay.deleteSpectroMeter(self)

    ##-\-\-\-\
    ## ACTIONS
    ##-/-/-/-/

    # ------------------------------
    # Open the spectrum graph window
    def openGraph(self):

        # Open the dock
        _open_dock = True
        if "spectrum" in self.parent.docks.keys():
            if self.parent.docks["spectrum"] is not None:
                _open_dock = False

        if _open_dock:
            self.parent.docks["spectrum"] = SpectrumDisplayPanel("Spectrum Display", self.parent)
            self.parent.addDockWidget(qtc.Qt.RightDockWidgetArea, self.parent.docks["spectrum"])

            # Set the size and attach the dock
            self.parent.docks["spectrum"].setFloating(True)
            #self.parent.docks["spectrum"].detectLocationChange()
            #self.parent.docks["spectrum"].setFloating(False)

    # --------------------------------
    # Open the settings of the syringe
    def openSettings(self):
        openWindow(self.parent, editSpectroMeterWindow, 'spectrometer', spectrometer=self.spectrometer)
