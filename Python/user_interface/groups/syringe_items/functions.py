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
from user_interface.popups.notifications import warningProceedMessage
from user_interface.equipment_config.syringe_pump.printed_pump.display import setArduinoSyringeWindow
from user_interface.equipment_config.flow_meter.display import setFlowMeterWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class SyringeGroupFunctions(object):

    ##-\-\-\-\-\-\
    ## CONTROL PUMP
    ##-/-/-/-/-/-/

    # --------------------------------
    # Send the run command to the pump
    def sendRunCommand(self, direction=1):

        # Set the speed if not running
        if not self.syringe.is_running:
            self.sendSetSpeedCommand()

        # Get the value
        volume = self.volumeEntry.text()
        if volume == 'ALL':
            volume = self.syringe.equipment.volume * 1000
        else:
            volume = float( volume )

        # Apply the direction
        volume = volume * direction

        # Rectify by the unit
        if self.syringe.equipment.unit.split('/')[0] == 'mL':
            volume = volume / 1000

        self.syringe.run(volume)

    # --------------------------------
    # Send the stop command to the pump
    def sendStopCommand(self):
        self.syringe.stop()

    # -------------------------------------
    # Send the setSpeed command to the pump
    def sendSetSpeedCommand(self):

        # Save the value
        self.syringe.equipment.editSetSpeed( self.speedEntry.value() )

        # Send the command
        self.syringe.setSpeed(priority=True)

    ##-\-\-\-\-\-\-\-\-\
    ## CONTROL FLOWMETER
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Send the read command to the flowmeter
    def sendStartReadCommand(self, direction=1):

        # Change the status
        self.flowmeter.is_running = True
        self.flowmeter.read_values = True

        # Send the command
        self.flowmeter.read()

    # --------------------------------
    # Send the stop command to the pump
    def sendStopReadCommand(self):
        self.flowmeter.is_running = False
        self.flowmeter.read_values = False

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # -------------
    # Display speed
    def displaySpeed(self):

        # Update the spinbox
        self.speedEntry.setValue(self.syringe.equipment.set_speed)

        # Update the label
        self.speedUnitLabel.setText( self.syringe.equipment.unit )

    # --------------------
    # Display acceleration
    def displayAccel(self):

        # Build the text
        accel_text = str(self.syringe.equipment.acceleration) + ' ' + self.syringe.equipment.unit + '²'

        # Update the interface
        #self.accelerationLabel.setText( accel_text )

    # ------------------------------------
    # Update the color of the progress bar
    def updateRunning(self):

        # Load the palette
        palette = qtg.QPalette( self.capacityProgressBar.palette() )

        # Check the status
        if self.syringe.is_running:
            palette.setColor(qtg.QPalette.Highlight, qtg.QColor("#499970"))

        else:
            palette.setColor(qtg.QPalette.Highlight, qtg.QColor("#418AAB"))

        # Assign the palette
        self.capacityProgressBar.setPalette(palette)

    # ------------------------------------------------
    # Update the volume entry when the slider is moved
    def updateVolumeEntry(self):

        # Get the volume from the slider
        new_volume = self.volumeSlider.value()

        # Special case: 100%
        if new_volume >= 100:
            new_volume = self.syringe.equipment.volume * 1000
            new_volume_text = 'ALL'

        # Convert into volume
        else:

            # Convert into log
            if new_volume != 0:
                new_volume = (np.exp(new_volume / 10) - 1)/(np.exp(10)-1)

            new_volume = self.syringe.equipment.volume * new_volume * 1000
            new_volume = round(new_volume, 2)
            new_volume_text = str(new_volume)

        # Save values in variables
        self.syringe.equipment.set_volume = new_volume
        self.syringe.equipment.set_volume_perc = new_volume * 100 / (self.syringe.equipment.volume * 1000)
        self.syringe.equipment.set_volume_text = new_volume_text

        # Replace the value of the Entry
        self.volumeEntry.setText( new_volume_text )

    # ---------------------------------------------------
    # Update the volume slider when the entry is modified
    def updateVolumeSlider(self):

        # Get the value of the entry
        new_entry = self.volumeEntry.text()
        new_entry = new_entry.strip()

        # Check if input is ALL
        if new_entry.lower() == 'all':
            new_entry = 'ALL'
            new_entry_value = 100

        # Convert the input
        else:
            try:
                # Convert the value
                new_entry_value = float(new_entry)
                new_entry_value = new_entry_value / (self.syringe.equipment.volume * 1000)
                if new_entry_value != 0:
                    new_entry_value = 10 * np.log( new_entry_value * (np.exp(10) - 1) + 1 )

                # Coerce the value
                if new_entry_value >= 100:
                    new_entry = 'ALL'
                    new_entry_value = 100

            # Get value from memory if incorrect
            except:
                new_entry = self.syringe.equipment.set_volume_text
                new_entry_value = self.syringe.equipment.set_volume_perc

        # Replace the variables
        self.syringe.equipment.set_volume = new_entry_value * self.syringe.equipment.volume * 1000 / 100
        self.syringe.equipment.set_volume_text = new_entry
        self.syringe.equipment.set_volume_perc = new_entry_value

        # Update the UI
        self.volumeEntry.setText( new_entry )
        self.volumeSlider.setValue( new_entry_value )

    # --------------------
    # Update the flow rate
    def updateFlowRate(self, value):

        # Update the text display
        try:
            text_value = "{:.2f}".format(round(value, 2))
            self.flowRateDisplay.setText( text_value )
        except:
            pass

    # -------------------------
    # Display the flowrate unit
    def displayUnit(self):
        try:
            self.flowUnitLabel.setText( self.flowmeter.unit )
        except:
            pass

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## GENERATE CONTEXT MENU
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Display the menu on a right click
    def showRightClickMenu(self, event):

        # Initialise the menu
        self.menu = qtw.QMenu()
        self.menu.setToolTipsVisible(True)

        # Delete the group
        rename_action = self.menu.addAction("Rename Syringe pump")
        rename_action.setToolTip('Edit the name of the pump')
        rename_action.setStatusTip('Edit the name of the pump')
        rename_action.triggered.connect(self.renameItem)

        # Delete the group
        delete_action = self.menu.addAction("Remove Syringe pump")
        delete_action.setToolTip('Remove the pump')
        delete_action.triggered.connect(self.deleteItem)
        
        self.menu.addSeparator()

        # Assign a flowmeter
        assign_flowmeter_action = self.menu.addAction("Flowmeter Sync.")
        assign_flowmeter_action.setToolTip('Synchronise the pump with a flowmeter to enable the PID controller')
        assign_flowmeter_action.triggered.connect(self.assignFlowmeter)

        if self.syringe.equipment.assigned_flowmeter is not None:
            discard_flowmeter_action = self.menu.addAction("De-sync. Flowmeter")
            discard_flowmeter_action.triggered.connect(self.desyncFlowmeter)

        # Display the menu at the mouse location
        action = self.menu.exec_(self.mapToGlobal(event))

    # ----------------
    # Delete the group
    def deleteItem(self):

        # Prompt the user
        ok = warningProceedMessage('Delete Syringe pump', 'Are you sure you want to disconnect and delete the selected syringe pump?')

        if ok:
            self.parent.groupDisplay.deleteSyringe(self)

    # ----------------
    # Rename the group
    def renameItem(self):

        # Prompt the user
        text, ok = qtw.QInputDialog.getText(self, 'Rename Syringe Pump', 'Name:', text=self.syringe.name)

        # Apply the change
        if ok:
            self.syringe.name = text
            self.parent.groupDisplay.refreshUI()

    ##-\-\-\-\
    ## ACTIONS
    ##-/-/-/-/

    # --------------------------------
    # Open the settings of the syringe
    def openSettings(self):
        openWindow(self.parent, setArduinoSyringeWindow, 'syringe_group', syringe_class=self.syringe, syringe_display=self)

    # ----------------------------------------------
    # Assign a Flowmeter to the current syringe pump
    def assignFlowmeter(self):

        # Prompt the user selection
        flowmeter_list = [x.name + ' (' + x.ftype + ', ' + x.serial_port + ')' for x in self.parent.equipments['flow_meter']]
        user_choice, valid = qtw.QInputDialog.getItem(self.parent, "Select Flowmeter", "Flowmeter(s):", flowmeter_list, 0, False)

        if valid:

            # Get the flowmeter
            flowmeter_id = flowmeter_list.index(user_choice)
            synced_flowmeter = self.parent.equipments['flow_meter'][flowmeter_id]

            # De-sync any existing pump
            if synced_flowmeter.assigned_pump is not None:
                synced_flowmeter.assigned_pump.desyncFlowmeter()

            # Assign the flowmeter and the pump
            self.syringe.equipment.assignFlowmeter( synced_flowmeter )

            # Refresh the UI
            self.parent.groupDisplay.refreshUI()

    # ----------------------------
    # De-synchronise the flowmeter
    def desyncFlowmeter(self):

        # Reload the flowmeter
        desynced_flowmeter = self.syringe.equipment.sync_flowmeter

        # Detach the flowmeter and the pump
        self.syringe.equipment.desyncFlowmeter()

        # Reload the flowmeter in the interface
        self.parent.groupDisplay.addFlowMeter( desynced_flowmeter )

        # Refresh the UI
        self.parent.groupDisplay.refreshUI()

    # ----------------------------------
    # Open the settings of the flowmeter
    def openFlowmeterSettings(self):
        openWindow(self.parent, setFlowMeterWindow, 'flow_meter', flowmeter=self.flowmeter)