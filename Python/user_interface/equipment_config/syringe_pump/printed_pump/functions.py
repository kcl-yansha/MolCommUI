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

from settings.equipment.syringe_calibration import getSyringeTypeList
from settings.equipment.gearbox_calibration import getGearboxesList

from user_interface._common_functions.path_to_assets import getIcon
from user_interface._common_functions.window_handling import openWindow
from user_interface.popups.notifications import warningProceedMessage, errorMessage
from user_interface.popups.load_settings.syringe_pump.display import loadSyringePumpSettingsWindow
from user_interface.popups.save_settings.syringe_pump.display import saveSyringePumpSettingsWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setArduinoSyringeFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## HANDLE MOVEMENT BUTTONS
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ---------------
    # Start the timer
    def movebutton_pressed(self, direction=1):

        # Set the direction
        self.move_direction = direction

        # Start the timer
        self.timer.start(self.timer_timeout)

        # Make the first movement
        self.arduino_syringe.jog(self.move_direction)

    # -------------------
    # Interrupt the timer
    def movebutton_released(self):
        self.timer.stop()

    # ----------------------
    # Increase the held time
    def movebutton_event_check(self):
        self.arduino_syringe.jog(self.move_direction)

    ##-\-\-\-\-\
    ## REFRESH UI
    ##-/-/-/-/-/

    # -------------------------------------
    # Update the list syringe type checkbox
    def refreshSyringeTypeList(self):
        self.syringeTypeComboBox.addItems( getSyringeTypeList() )

    # --------------------------------
    # Update the list gearbox checkbox
    def refreshGearboxList(self):
        self.gearboxComboBox.addItems( getGearboxesList() )

    # ---------------------
    # Update the properties
    def updateProperties(self):

        # Display the syringe name and board
        self.syringePumpName.setText( self.arduino_syringe.name )

        # Get the current syringe properties
        self.boardLabel.setText( self.arduino_syringe.syringe_group.name + ' (' + self.arduino_syringe.axis + ')' )

        # Display the syringe properties
        self.syringeTypeComboBox.setTextValue(self.arduino_syringe.equipment.stype)
        self.speedSpinBox.setValue(self.arduino_syringe.equipment.speed)
        self.speedUnitComboBox.setTextValue(self.arduino_syringe.equipment.unit)
        self.accelerationSpinBox.setValue(self.arduino_syringe.equipment.acceleration)
        self.gearboxComboBox.setTextValue(self.arduino_syringe.equipment.geartype)

    # -------------------------------------
    # Save the current settings when called
    def saveCurrentSettings(self):

        # Prepare the variables for change
        _edit_speed = False
        _edit_acceleration = False

        # Compare each of the parameters with the class - replace if different
        crt_type = self.syringeTypeComboBox.currentText()
        if crt_type != self.arduino_syringe.equipment.stype:

            self.arduino_syringe.equipment.stype = crt_type
            self.arduino_syringe.equipment.updateSyringeType()

            _edit_speed = True
            _edit_acceleration = True

        crt_gear = self.gearboxComboBox.currentText()
        if crt_gear != self.arduino_syringe.equipment.geartype:

            self.arduino_syringe.equipment.geartype = crt_gear
            self.arduino_syringe.equipment.updateGearboxType()

            _edit_speed = True
            _edit_acceleration = True

        crt_acceleration = self.accelerationSpinBox.value()
        if crt_acceleration != self.arduino_syringe.equipment.acceleration:
            self.arduino_syringe.equipment.acceleration = crt_acceleration
            _edit_acceleration = True

        crt_unit = self.speedUnitComboBox.currentText()
        if crt_unit != self.arduino_syringe.equipment.unit:
            self.arduino_syringe.equipment.unit = crt_unit
            _edit_speed = True
            _edit_acceleration = True

        crt_speed = self.speedSpinBox.value()
        if crt_speed != self.arduino_syringe.equipment.speed:

            self.arduino_syringe.equipment.set_speed = crt_speed
            self.arduino_syringe.equipment.editSpeed( crt_speed )

            _edit_speed = True

        # Save and edit the name of the pump
        self.arduino_syringe.name = self.syringePumpName.text()
        self.arduino_syringe.equipment.name = self.syringePumpName.text()
        self.arduino_syringe.getFileInfos()

        return _edit_speed, _edit_acceleration

    ##-\-\-\-\-\-\-\-\
    ## SYRINGE SETTINGS
    ##-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Open the submenu for saving the settings
    def getSaveSettingsMenu(self):

        # Save the current settings
        self.saveCurrentSettings()

        # Open the window
        openWindow(self.parent, saveSyringePumpSettingsWindow, 'save_settings', syringe_group=self.arduino_syringe.syringe_group, syringe_axis=self.arduino_syringe.axis)

    # ----------------------------------------
    # Open the submenu for saving the settings
    def getLoadSettingsMenu(self):
        openWindow(self.parent, loadSyringePumpSettingsWindow, 'load_settings', interface=self, syringe_group=self.arduino_syringe.syringe_group, syringe_axis=self.arduino_syringe.axis)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ----------------------------------------------
    # Apply the new settings to the existing syringe
    def applySettings(self):

        # Save all the changes
        _edit_speed, _edit_acceleration = self.saveCurrentSettings()

        # Apply the change to the Arduino
        if _edit_speed:
            self.arduino_syringe.setSpeed()

        if _edit_acceleration:
            self.arduino_syringe.setAccel()

        # Add a line
        if _edit_speed or _edit_acceleration:
            print('--------------------')

        # Update the main window interface
        if self.display_type == 'syringe_group':
            self.syringe_display.setTitle( self.arduino_syringe.name )
            self.syringe_display.displaySpeed()
            self.syringe_display.displayAccel()

        else:
            self.syringe_display.nameLabel.setText('- ' + self.arduino_syringe.name)

        # Close the window
        self.close()
