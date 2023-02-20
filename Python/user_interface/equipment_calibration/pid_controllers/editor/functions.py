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

from settings.equipment.pid_calibration import getDefaultCalibration, getPIDList, savePIDConfig, loadPIDCalibrationConfig

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class editPIDCalibrationFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # ---------------------
    # Initialise the window
    def initialiseWindow(self, controller_name=None):

        # Set default for a new PID controller
        if controller_name is None:

            # Edit the name
            self.nameEntry.setText('New controller')
            self.check_name = True

            # Load the values
            calibration_dict = getDefaultCalibration()

        else:

            # Edit the name
            self.nameEntry.setText(controller_name)
            self.nameEntry.setDisabled(True)
            self.check_name = False

            # Load the values
            calibration_dict = loadPIDCalibrationConfig(controller_name)

        # Edit the window content
        self.pValueEntry.setValue(calibration_dict['p_coeff'])
        self.iValueEntry.setValue(calibration_dict['i_coeff'])
        self.dValueEntry.setValue(calibration_dict['d_coeff'])

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------
    # Save the settings
    def saveSettings(self):

        # Get the values
        controller_name = self.nameEntry.text()
        controller_dict = {
        # General
        'p_coeff':self.pValueEntry.value(),
        'i_coeff':self.iValueEntry.value(),
        'd_coeff':self.dValueEntry.value(),
        }

        # Check that the name if accepted
        if self.check_name:

            # Get the list of names in the memory
            all_names = getPIDList()

            # Raise an issue if the name exist
            if controller_name.lower() == 'default':
                errorMessage("Invalid Name", "Default cannot be used as a gearbox name.")
                return 0

            # Raise an issue if the name exist
            if controller_name in all_names:
                errorMessage("Invalid Name", controller_name + " is already used as a gearbox name.")
                return 0

        # Save the value in file
        savePIDConfig(controller_name, controller_dict)

        # Apply the change
        for opened_meter in self.parent.equipments['flow_meter']:
            opened_meter.updatePIDType()

        # Close the window
        self.close()

        # Reload the parent window
        if self.manager is not None:
            self.manager.fillControllerTable()
