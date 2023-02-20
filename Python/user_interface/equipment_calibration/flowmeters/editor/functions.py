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

from settings.equipment.flowmeter_calibration import getFlowmeterTypeInfos, saveFlowmeterConfig, loadFlowmeterCalibrationConfig

from user_interface.popups.notifications import errorMessage, warningProceedMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class editFlowmeterCalibrationFunction(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # ---------------------
    # Initialise the window
    def initialiseWindow(self, flowmeter_serial=None):

        # Set default for a new syringe
        if flowmeter_serial is None:

            # Edit the status
            self.portComboBox.setEnabled(True)
            self.refreshButton.setEnabled(True)
            self.connectButton.setEnabled(True)
            self.flowMeterName.setEnabled(True)
            self.check_name = True

            # Preload the values
            self.calibrationEntry.setText( "1.0" )

        else:

            # Edit the status
            self.portComboBox.setEnabled(False)
            self.refreshButton.setEnabled(False)
            self.connectButton.setEnabled(False)
            self.flowMeterName.setEnabled(False)
            self.check_name = False

            # Load the values
            if flowmeter_serial in getFlowmeterTypeInfos():
                calibration_dict = loadFlowmeterCalibrationConfig(flowmeter_serial)
            else:
                calibration_dict = {
                'type':'SLI-0430',
                'calibration_factor':1.0
                }

            # Edit the window content
            self.flowMeterName.setText( flowmeter_serial )
            self.typeComboBox.setTextValue( calibration_dict['type'] )
            self.calibrationEntry.setText( str(calibration_dict['calibration_factor']) )

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
    def checkFlowMeter(self):

        # Get the port
        open_port = self.portComboBox.currentText()
        print('Checking '+open_port+'...')

        # Check if the port has already been loaded
        if open_port in self.parent.active_ports:
            errorMessage("Port already open", "The selected port has already been loaded.")

        # Try checking the port
        try:

            # Try opening the port
            opened_meter = loadFlowMeterClass(self.parent, open_port, debug=self.parent.main_config['debug_flowmeter'])

            # Update the button text
            serial_number = opened_meter.serial_number

            # Close the connection
            opened_meter.close()

            # Ask for confirmation
            if warningProceedMessage("Flowmeter Detected","A flowmeter was detected, with the Serial Number "+str(serial_number)+'. Do you want to load it?'):
                self.flowMeterName.setText(serial_number)

        except:
            pass

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------
    # Save the settings
    def saveSettings(self):

        # Get the values
        flowmeter_name = self.flowMeterName.text()
        flowmeter_dict = {
        # General
        'type':self.typeComboBox.currentText(),
        # Settings
        'calibration_factor':float( self.calibrationEntry.text() ),
        }

        # Check that the name if accepted
        if self.check_name:

            # Get the list of names in the memory
            all_names = getFlowmeterTypeInfos()

            # Raise an issue if there is no name
            if flowmeter_name.lower() == '':
                errorMessage("Invalid S/N", "You must specify a serial number for the flowmeter.")
                return 0

            # Raise an issue if the name exist
            if flowmeter_name.lower() == 'default':
                errorMessage("Invalid S/N", "Default cannot be used as a flowmeter serial number.")
                return 0

            # Raise an issue if the name exist
            if flowmeter_name in all_names:
                errorMessage("Invalid S/N", flowmeter_name + " is already saved in the memory.")
                return 0

        # Save the value in file
        saveFlowmeterConfig(flowmeter_name, flowmeter_dict)

        # Close the window
        self.close()

        # Reload the parent window
        if self.manager is not None:
            self.manager.fillFlowmeterTable()
