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

from equipment.spectrometer.commands import get_list_spectrometers
from equipment.spectrometer.equipment_class import loadSpectroMeterClass

from user_interface._common_functions.path_to_assets import getIcon
from user_interface.popups.notifications import warningProceedMessage, errorMessage

from settings.equipment.reload_equipment import addPort

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setSpectroMeterFunctions(object):

    ##-\-\-\-\-\
    ## CONNECTION
    ##-/-/-/-/-/

    # --------------------------------------
    # Refresh the port list in the combo box
    def refreshPortList(self):

        # List of ports
        self.active_ports = get_list_spectrometers()

        # Fills the combo box
        self.portComboBox.clear()
        self.portComboBox.addItems(self.active_ports)

    # -----------------------------------
    # Change the status of the connection
    def connectSpectrometer(self):

        # Reinitialise the connection
        if self.connected:

            # Delete and remove from parent if in the list
            if self.is_loaded:

                try:
                    self.parent.equipments['spectrometer'].remove(self.spectrometer)
                    self.parent.active_ports.remove(self.spectrometer.serial_port)

                    # Update the button text
                    self.closeButton.setText('Close')

                except:
                    pass

            # Close the connection
            self.spectrometer.close()

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
                opened_meter = loadSpectroMeterClass(self.parent, open_port, debug=self.parent.main_config['debug_flowmeter'])

                # Load the flowmeter is found
                if opened_meter is not None:
                    self.spectrometer = opened_meter

                    # Update the properties
                    self.connected = True

                    # Update the UI
                    self.setSpectrometerInfos()

                # Raise an error otherwise
                else:
                    errorMessage("Spectrometer not found", "No Spectrometer was detected at the given port.")

        # Update the display
        self.updateConnectButton()

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

            self.closeButton.setText('Cancel')

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
        self.spectroMeterName.setEnabled(properties_status)
        self.delaySpinBox.setEnabled(properties_status)

        # User control
        self.setButton.setEnabled(properties_status)

    # ---------------------------------------
    # Set the information of the spectrometer
    def setSpectrometerInfos(self):

        # Set the text
        self.spectroMeterName.setText(self.spectrometer.name)
        self.spectroMeterModel.setText( 'Model: ' + self.spectrometer.model )
        self.spectroMeterPixels.setText( 'Pixels: ' + str(self.spectrometer.n_pixels) )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # --------------------------------------
    # Save the details in a new spectrometer
    def saveSpectroMeter(self):

        # Save the current settings
        self.spectrometer.name = self.spectroMeterName.text()
        self.spectrometer.setIntegrationTime( self.integrationSpinBox.value() )
        self.spectrometer.delay_time = self.delaySpinBox.value()

        print(self.spectrometer.name, self.spectrometer.serial_number)

        # Update if needed
        if not self.is_loaded:

            # Set the port as active
            self.parent.active_ports.append( self.spectrometer.serial_number )
            print('Connected to '+self.spectrometer.serial_number+' with name '+self.spectrometer.name)
            print('--------------------')

            # Add the spectrometer to the connected spectrometer
            self.parent.equipments['spectrometer'].append(self.spectrometer)

            # Add the flowmeter to the equipment recently loaded
            spectrometer_dict = {
            'equipment_type': 'spectrometer',
            'name': self.spectrometer.name,
            'serial': self.spectrometer.serial_number,
            'integration': self.spectrometer.integration_time,
            'delay': self.spectrometer.delay_time
            }
            addPort( self.spectrometer.serial_number, spectrometer_dict, user_name=self.parent.main_config['current_user'] )

            # Update the main window
            self.parent.groupDisplay.addSpectroMeter( self.spectrometer )

        # Close the window
        self.to_load = True
        self.close()
