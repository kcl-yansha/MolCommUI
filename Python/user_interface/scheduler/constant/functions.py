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

from multithreading.scheduler.events import Constant

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setConstantFunctions(object):

    ##-\-\-\-\-\-\-\
    ## INIT INTERFACE
    ##-/-/-/-/-/-/-/

    # ----------------------
    # Populate the interface
    def initInterface(self):

        if self.event is not None:

            # Apply all the values
            self.valueFlowrate.setValue( self.event.value )
            self.valueDuration.setValue( self.event.duration )

            # Set the status of the box
            self.valueDurationCheckbox.setChecked( self.event.duration != 0 )

        self.updateDurationSelection()

    # ---------------------------------------
    # Populate the display with all the pumps
    def populatePumpList(self):

        # Reset the display
        for i in reversed(range(self.pumpListLayout.count())):
            self.pumpListLayout.itemAt(i).widget().setParent(None)

        # Process all the books
        self.pumpCheckBoxes = []
        for pump in self.parent.equipments['syringe_pumps']:

            # Make the widget
            pumpCheckBox = qtw.QCheckBox(pump.name)
            if self.event is not None:
                if pump in self.event.pumps:
                    pumpCheckBox.setChecked(True)

            # Add to the interface
            self.pumpCheckBoxes.append([pumpCheckBox, pump])
            self.pumpListLayout.addWidget( pumpCheckBox )

    ##-\-\-\-\-\-\-\
    ## EDIT INTERFACE
    ##-/-/-/-/-/-/-/

    # ---------------------------------
    # Update the status of the checkbox
    def updateDurationSelection(self):
        self.valueDuration.setEnabled( self.valueDurationCheckbox.isChecked() )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -------------------
    # Read all the values
    def _read_values(self):

        # Get the pumps
        selected_pumps = []
        for box, pump in self.pumpCheckBoxes:
            if box.isChecked():
                selected_pumps.append(pump)

        # Get the values
        value = self.valueFlowrate.value()

        if self.valueDurationCheckbox.isChecked():
            duration = self.valueDuration.value()
        else:
            duration = 0

        return selected_pumps, value, duration

    # ------------------------------
    # Edit the settings of the pulse
    def setConstant(self):

        # Retrieve all the values
        selected_pumps, value, duration = self._read_values()

        if len(selected_pumps) == 0:
            errorMessage('No pump selected','Please select at least one pump to proceed.')
            return 0

        # Create a new event
        if self.event is None:

            # Create the new event
            new_event = Constant(selected_pumps, value, duration)

            # Add to the list
            self.parent_widget.addEvent(new_event)

        # Edit the existing event
        else:

            # New values
            self.event.pumps = selected_pumps
            self.event.value = value
            self.event.duration = duration

            # Regenerate the values
            self.event.getCommands()
            self.event.getDescription()

        # Refresh the display
        self.close()
        self.parent_widget.fillEventTable()
