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
from equipment.flow_meter.equipment_class import loadFlowMeterClass
from equipment.flow_meter.properties import getFlowMeterType

from user_interface._common_functions.path_to_assets import getIcon
from user_interface._common_functions.window_handling import openWindow
from user_interface.popups.notifications import warningProceedMessage, errorMessage, errorProceedMessage

from user_interface.equipment_calibration.flowmeters.editor.display import editFlowmeterCalibrationWindow

from settings.equipment.flowmeter_calibration import getFlowmeterTypeInfos, loadFlowmeterCalibrationConfig
from settings.equipment.reload_equipment import addPort
from settings.equipment.pid_calibration import getPIDList

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setFlowMeterFunctions(object):

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
    def connectFlowMeter(self):

        # Reinitialise the connection
        if self.connected:

            # Delete and remove from parent if in the list
            if self.is_loaded:

                try:
                    self.parent.equipments['flow_meter'].remove(self.flowmeter)
                    self.parent.active_ports.remove(self.flowmeter.serial_port)

                    # Update the button text
                    self.closeButton.setText('Close')

                except:
                    pass

            # Close the connection
            self.flowmeter.close()

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
                opened_meter = loadFlowMeterClass(self.parent, open_port, debug=self.parent.main_config['debug_flowmeter'])

                # Load the flowmeter is found
                if opened_meter is not None:
                    if opened_meter.serial_number in list(getFlowmeterTypeInfos().keys()):

                        self.flowmeter = opened_meter

                        # Apply the calibration
                        calibration_dict = getFlowmeterTypeInfos()
                        self.typeComboBox.setTextValue(calibration_dict[opened_meter.serial_number]['type'])

                        # Update the properties
                        self.connected = True
                        self.setFlowMeter()

                        # Update the UI
                        self.flowMeterName.setText(self.flowmeter.name)

                    # Raise an error if the flowmeter is not listed
                    else:

                        # Close the session
                        opened_meter.close()

                        # Ask the user to save the config
                        if errorProceedMessage('Unknown S/N', 'The Flowmeter Serial Number '+opened_meter.serial_number+' has not be configured yet. Do you want to close this window and configure settings for it?'):

                            # Close the current window
                            self.close()

                            # Open the new window
                            openWindow(self.parent, editFlowmeterCalibrationWindow, 'edit_flowmeter', calibration_manager=None, flowmeter_serial=opened_meter.serial_number)

                # Raise an error otherwise
                else:
                    errorMessage("Flow meter not found", "No Flow meter was detected at the given port.")

        # Update the display
        self.updateConnectButton()

    ##-\-\-\-\-\
    ## REFRESH UI
    ##-/-/-/-/-/

    # -----------------------------------
    # Update the list controller checkbox
    def refreshPIDList(self):
        self.PIDControllerComboBox.addItems( getPIDList() )

    # ---------------------------------
    # Update the look of the pushbutton
    def updateConnectButton(self):

        # Change to disconnect
        if self.connected:
            self.connectButton.setColor('#8C2E2E')
            self.connectButton.setIcon( getIcon('connect_status_on.png') )
            self.connectButton.setToolTip("Disconnect from the selected port.")
            self.connectButton.setText('Disconnect')

            self.closeButton.setText('Cancel')

            self.updateProperties()

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

        # Properties controls
        self.typeComboBox.setEnabled(properties_status)
        self.flowMeterName.setEnabled(properties_status)
        self.delaySpinBox.setEnabled(properties_status)
        self.filterSettingsWidget.setEnabled(properties_status)

        # User control
        self.setButton.setEnabled(properties_status)

    # ---------------------
    # Update the properties
    def updateProperties(self):

        # Display the flowmeter properties
        self.flowMeterName.setText(self.flowmeter.name)

        self.typeComboBox.setTextValue(self.flowmeter.ftype)
        self.serialNumberEntry.setText(self.flowmeter.serial_number)

        self.delaySpinBox.setValue(self.flowmeter.delay)

        self.PIDControllerComboBox.setTextValue(self.flowmeter.pid_controller)

        self.filterSettingsWidget.setChecked(self.flowmeter.use_previous)
        self.filterValueSpinBox.setValue(self.flowmeter.n_previous)

    ##-\-\-\-\-\-\-\-\-\-\
    ## FLOWMETER SELECTION
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------
    # Set the flow meter type
    def setFlowMeter(self):

        # Check if the flowmeter is connected
        if self.connected:

            # Get the flowmeter type from the combo box
            flowmeter_type = self.typeComboBox.currentText()
            self.flowmeter.ftype = flowmeter_type

            # Get the info
            flowmeter_properties = getFlowMeterType()
            flowmeter_properties = flowmeter_properties[flowmeter_type]

            # Update the flow meter properties
            self.flowmeter.chip = flowmeter_properties['chip']
            self.flowmeter.scale_factor = flowmeter_properties['scale_factor']
            self.flowmeter.min_range = flowmeter_properties['min_range']
            self.flowmeter.max_range = flowmeter_properties['max_range']
            self.flowmeter.unit = flowmeter_properties['unit']

            self.flowmeter.delay = self.delaySpinBox.value()

            crt_pid = self.PIDControllerComboBox.currentText()
            if crt_pid != self.flowmeter.pid_controller:
                self.flowmeter.pid_controller = crt_pid
                self.flowmeter.updatePIDType()

            self.flowmeter.use_previous = self.filterSettingsWidget.isChecked()
            self.flowmeter.n_previous = self.filterValueSpinBox.value()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------------------------
    # Save the details in a new syringe group
    def saveFlowMeter(self):

        # Save the current settings
        self.flowmeter.name = self.flowMeterName.text()
        self.setFlowMeter()

        # Update if needed
        if not self.is_loaded:

            # Initialise the flowmeter
            self.flowmeter.init(self.flowmeter.ftype)

            # Set the port as active
            self.parent.active_ports.append( self.flowmeter.serial_port )
            print('Connected to '+self.flowmeter.serial_port+' with name '+self.flowmeter.name + ' (S/N: '+ self.flowmeter.serial_number +')')
            print('--------------------')

            # Add the flow meter to the connected elements
            self.parent.equipments['flow_meter'].append(self.flowmeter)

            # Update the main window
            self.parent.groupDisplay.addFlowMeter( self.flowmeter )

        else:
            self.parent.groupDisplay.refreshUI()

        # Add the flowmeter to the equipment recently loaded
        flowmeter_dict = {
        'equipment_type': 'flowmeter',
        'name': self.flowmeter.name,
        'ftype': self.flowmeter.ftype,
        'pid': self.flowmeter.pid_controller,
        'filter-use': self.flowmeter.use_previous,
        'filter-wsize': self.flowmeter.n_previous
        }
        addPort( self.flowmeter.serial_port, flowmeter_dict, user_name=self.parent.main_config['current_user'] )

        # Close the window
        self.to_load = True
        self.close()
