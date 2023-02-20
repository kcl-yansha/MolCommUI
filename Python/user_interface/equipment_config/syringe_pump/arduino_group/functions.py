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

from equipment.connection.arduino import get_list_ports
from equipment.syringe_pump.equipment_class import SyringeEquipment, loadSyringeGroupClass

from settings.equipment.syringe_calibration import getSyringeTypeList
from settings.equipment.gearbox_calibration import getGearboxesList
from settings.equipment.reload_equipment import addPort

from user_interface._common_functions.path_to_assets import getIcon
from user_interface._common_functions.window_handling import openWindow
from user_interface.popups.notifications import warningProceedMessage, errorMessage
from user_interface.popups.load_settings.syringe_group.display import loadSyringeSettingsWindow
from user_interface.popups.save_settings.syringe_group.display import saveSyringeSettingsWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setArduinoGroupFunctions(object):

    ##-\-\-\-\-\
    ## CONNECTION
    ##-/-/-/-/-/

    # --------------------------------------
    # Refresh the port list in the combo box
    def refreshPortList(self):

        # List of ports
        self.active_ports = get_list_ports()

        # Fills the combo box
        self.portComboBox.clear()
        self.portComboBox.addItems(self.active_ports)

    # -----------------------------------
    # Change the status of the connection
    def connectGroup(self):

        # Reinitialise the connection
        if self.connected:

            # Close the connection
            self.arduino_group.close()

            # Reinitialise the parameters
            self.connected = False

        # Establish the connection to the pump
        else:

            # Get the port
            open_port = self.portComboBox.currentText()
            print('Connecting to '+open_port+'...')

            # Check if the port has already been loaded
            if open_port in self.parent.active_ports:
                errorMessage("Port already open", "The selected port has already been loaded.")

            else:

                # Try opening the port
                opened_group = loadSyringeGroupClass(self.parent, open_port)

                # Load the group is found
                if opened_group is not None:
                    self.arduino_group = opened_group

                    # Update the properties
                    self.connected = True
                    self.updateProperties()

                # Raise an error otherwise
                else:
                    errorMessage("Syringe pump not found", "No Arduino-based syringe pump was detected at the given port.")

        # Update the display
        self.updateConnectButton()

    ##-\-\-\-\-\-\-\-\-\
    ## SYRINGE SELECTION
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Update the list syringe type checkbox
    def refreshSyringeTypeList(self):
        self.syringeTypeComboBox.addItems( getSyringeTypeList() )

    # --------------------------------
    # Update the list gearbox checkbox
    def refreshGearboxList(self):
        self.gearboxComboBox.addItems( getGearboxesList() )

    # -----------------------------------------------
    # Get the next syringe in the list and display it
    def getNextSyringe(self, increment=1):

        # Save everything before moving
        self.saveCurrentSettings()

        # Get the list of axis
        all_axis = self.arduino_group.getPorts()

        # Get the new index to display
        new_id = all_axis.index(self.axis) + increment
        if new_id < 0:
            new_id = len(all_axis) - 1
        elif new_id >= len(all_axis):
            new_id = 0

        # Get and display the new axis
        new_axis = all_axis[ new_id ]

        self.updateProperties( axis=new_axis )

    # --------------------------------------
    # Save the current settings in the class
    def saveCurrentSettings(self):

        # Save the parameters
        self.syringe.name = self.syringePumpName.text()
        self.syringe.stype = self.syringeTypeComboBox.currentText()
        self.syringe.unit = self.speedUnitComboBox.currentText()
        self.syringe.acceleration = self.accelerationSpinBox.value()
        self.syringe.geartype = self.gearboxComboBox.currentText()

        self.syringe.set_speed = self.speedSpinBox.value()
        self.syringe.editSpeed( self.speedSpinBox.value() )

        # Set the indirect values
        self.syringe.updateSyringeType()
        self.syringe.updateGearboxType()

        # Change the axis if needed
        if self.syringeAxisComboBox.currentText() != self.axis:

            # Save in the new axis
            new_axis = self.syringeAxisComboBox.currentText()
            self.arduino_group.syringes[ new_axis ] = self.arduino_group.syringes[ self.axis ]

            # Reset the old axis
            self.arduino_group.syringes[ self.axis ] = None
            self.axis = new_axis

    # ---------------------------------
    # Add a syringe on the missing port
    def addNewSyringe(self):

        # Get the list of empty axis
        all_axis = self.arduino_group.getPorts(empty=True)
        new_axis = all_axis[0]

        # Create a new syringe
        self.arduino_group.addSyringe(self.parent, axis=new_axis)

        # Display the new syringe
        self.updateProperties( axis=new_axis )
        self.updateNewDeleteButtonsStatus()

    # -----------------------------------------
    # Delete the current syringe from the group
    def deleteCurrentSyringe(self):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the section?','Are you sure you want to delete the selected syringe? All its properties will be lost.'):

            # Save the axis to delete
            crt_axis = self.axis

            # Move to the next syringe
            self.getNextSyringe()

            # Delete the syringe from the class
            self.arduino_group.syringes[crt_axis] = None

            # Refresh the button status
            self.updateNewDeleteButtonsStatus()
            self.updateAxisSelection()
            self.updateProperties(axis=self.axis)

    ##-\-\-\-\-\-\-\-\
    ## SYRINGE SETTINGS
    ##-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Open the submenu for saving the settings
    def getSaveSettingsMenu(self):

        # Save the current settings
        self.saveCurrentSettings()

        # Open the window
        openWindow(self.parent, saveSyringeSettingsWindow, 'save_settings', syringe_group=self.arduino_group, syringe_axis=self.axis)

    # ----------------------------------------
    # Open the submenu for saving the settings
    def getLoadSettingsMenu(self):
        openWindow(self.parent, loadSyringeSettingsWindow, 'load_settings', interface=self, syringe_group=self.arduino_group, syringe_axis=self.axis)

    ##-\-\-\-\-\
    ## REFRESH UI
    ##-/-/-/-/-/

    # ---------------------------------
    # Update the look of the pushbutton
    def updateConnectButton(self):

        # Change to disconnect
        if self.connected:
            self.connectButton.setColor('#8C2E2E')
            self.connectButton.setIcon( getIcon('connect_status_on.png') )
            self.connectButton.setToolTip("Disconnect from the selected port.")
            self.connectButton.setText('Disconnect')

        # Change to connect
        else:
            self.connectButton.setColor('#2d6f8b')
            self.connectButton.setIcon( getIcon('connect_status_off.png') )
            self.connectButton.setToolTip("Connect to the selected USB port.")
            self.connectButton.setText('Connect')

        # Update the rest of the controls
        self.updateEnabledStatus()

    # --------------------------------
    # Update the status of the control
    def updateEnabledStatus(self):

        # Get the new states
        connection_status = not self.connected
        properties_status = self.connected

        # Connection controls
        self.portComboBox.setEnabled(connection_status)
        self.refreshButton.setEnabled(connection_status)

        # Selection controls
        self.syringeGroupName.setEnabled(properties_status)
        self.previousSyringeButton.setEnabled(properties_status)
        self.nextSyringeButton.setEnabled(properties_status)
        self.syringePumpName.setEnabled(properties_status)
        self.saveSettingsButton.setEnabled(properties_status)
        self.loadSettingsButton.setEnabled(properties_status)

        # Properties controls
        self.syringeTypeComboBox.setEnabled(properties_status)
        self.speedSpinBox.setEnabled(properties_status)
        self.speedUnitComboBox.setEnabled(properties_status)
        self.accelerationSpinBox.setEnabled(properties_status)
        self.gearboxComboBox.setEnabled(properties_status)

        # User control
        self.setButton.setEnabled(properties_status)

        # Update the new and delete buttons
        self.updateNewDeleteButtonsStatus()
        self.updateAxisSelection()

    # ----------------------------------------------
    # Update the status of the new and delete button
    def updateNewDeleteButtonsStatus(self):

        # Disable if disconnected
        if not self.connected:
            self.newSyringeButton.setEnabled(False)
            self.deleteSyringeButton.setEnabled(False)

        # Check the status
        else:

            # Check the number of axis loaded
            n_axis = len( self.arduino_group.getPorts() )

            # Disable the new button
            if n_axis >= 3:
                self.newSyringeButton.setEnabled(False)
            else:
                self.newSyringeButton.setEnabled(True)

            # Disable the delete button
            if n_axis <= 1:
                self.deleteSyringeButton.setEnabled(False)
            else:
                self.deleteSyringeButton.setEnabled(True)

    # --------------------------------
    # Update the selection of the axis
    def updateAxisSelection(self):

        # Disable if disconnected
        if not self.connected:
            self.syringeAxisComboBox.setEnabled(False)

        # Check the status
        else:

            # Check the number of axis loaded
            n_axis = len( self.arduino_group.getPorts() )

            # Disable the combobox
            if n_axis >= 3:
                self.syringeAxisComboBox.setEnabled(False)

            # Enable and select the content
            else:
                self.syringeAxisComboBox.setEnabled(True)

            # Get the list of available axis
            available_axis = self.arduino_group.getPorts(empty=True)
            available_axis.append(self.axis)

            # Append the list
            self.syringeAxisComboBox.clear()
            self.syringeAxisComboBox.addItems( sorted(available_axis) )

    # ---------------------
    # Update the properties
    def updateProperties(self, axis='X'):

        # Display the syringe group name
        self.syringeGroupName.setText( self.arduino_group.name )

        # Get the current syringe properties
        self.axis = axis
        self.syringe = self.arduino_group.syringes[ self.axis ]

        # Refresh the axis selection
        self.updateAxisSelection()

        # Display the syringe properties
        self.syringePumpName.setText(self.syringe.name)
        self.syringeAxisComboBox.setTextValue(self.axis)
        self.syringeTypeComboBox.setTextValue(self.syringe.stype)
        self.speedSpinBox.setValue(self.syringe.speed)
        self.speedUnitComboBox.setTextValue(self.syringe.unit)
        self.accelerationSpinBox.setValue(self.syringe.acceleration)
        self.gearboxComboBox.setTextValue(self.syringe.geartype)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------------------------
    # Save the details in a new syringe group
    def saveSyringeGroup(self):

        # Save the current settings
        self.saveCurrentSettings()

        # Get the list of syringe being saved
        all_axis = self.arduino_group.getPorts()

        # Initialise the content of the syringe
        syringe_dict = {
        'equipment_type': 'syringe_pump',
        'name': self.arduino_group.name
        }

        # Save all the syringes
        for axis in all_axis:

            # Get the class
            crt_syringe = SyringeEquipment(self.arduino_group, axis_port=axis, debug=self.parent.main_config['debug_syringe_send'], verbose=self.parent.main_config['debug_syringe'])

            # Save the class
            equipment_name = self.arduino_group.serial_port + ' - ' + self.arduino_group.name + ' - ' + crt_syringe.name
            self.parent.equipments['syringe_pumps'].append(crt_syringe)

            # Set the different settings
            crt_syringe.setSpeed()
            crt_syringe.setAccel()

            # Update the main window
            self.parent.groupDisplay.addSyringe( crt_syringe )

            # Update the information to be saved
            syringe_dict[ axis+'_name' ] = crt_syringe.name
            syringe_dict[ axis+'_type' ] = crt_syringe.equipment.stype
            syringe_dict[ axis+'_gear' ] = crt_syringe.equipment.geartype
            syringe_dict[ axis+'_unit' ] = crt_syringe.equipment.unit
            syringe_dict[ axis+'_speed' ] = crt_syringe.equipment.speed
            syringe_dict[ axis+'_accel' ] = crt_syringe.equipment.acceleration

        # Set the port as active
        self.parent.active_ports.append( self.arduino_group.serial_port )
        print('Connected to '+self.arduino_group.serial_port+' with name '+self.arduino_group.name)
        print('--------------------')

        # Add the syringe pump to the equipment recently loaded
        addPort( self.arduino_group.serial_port, syringe_dict, user_name=self.parent.main_config['current_user'] )

        # Close the window
        self.to_load = True
        self.close()
