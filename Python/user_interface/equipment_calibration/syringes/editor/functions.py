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

from settings.equipment.syringe_calibration import getDefaultCalibration, getSyringeTypeList, saveSyringeGroupConfig, loadSyringeCalibrationConfig

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class editSyringeCalibrationFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # ---------------------
    # Initialise the window
    def initialiseWindow(self, syringe_name=None):

        # Set default for a new syringe
        if syringe_name is None:

            # Edit the name
            self.nameEntry.setText('New type')
            self.check_name = True

            # Load the values
            calibration_dict = getDefaultCalibration()

        else:

            # Edit the name
            self.nameEntry.setText(syringe_name)
            self.nameEntry.setDisabled(True)
            self.check_name = False

            # Load the values
            calibration_dict = loadSyringeCalibrationConfig(syringe_name)

        # Edit the window content
        self.volumeEntry.setValue(calibration_dict['volume'])
        self.diameterEntry.setValue(calibration_dict['diameter'])
        self.calibrationEntry.setText( str(calibration_dict['calibration_factor']) )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------
    # Save the settings
    def saveSettings(self):

        # Get the values
        syringe_name = self.nameEntry.text()
        syringe_dict = {
        # General
        'volume':self.volumeEntry.value(),
        'diameter':self.diameterEntry.value(),
        # Settings
        'calibration_factor':float( self.calibrationEntry.text() ),
        }

        # Check that the name if accepted
        if self.check_name:

            # Get the list of names in the memory
            all_names = getSyringeTypeList()

            # Raise an issue if the name exist
            if syringe_name.lower() == 'default':
                errorMessage("Invalid Name", "Default cannot be used as a syringe name.")
                return 0

            # Raise an issue if the name exist
            if syringe_name in all_names:
                errorMessage("Invalid Name", config_name + " is already used as a syringe name.")
                return 0

        # Save the value in file
        saveSyringeGroupConfig(syringe_name, syringe_dict)

        # Apply the change
        for opened_syringe in self.parent.equipments['syringe_pumps']:
            opened_syringe.equipment.updateSyringeType()

        # Close the window
        self.close()

        # Reload the parent window
        if self.manager is not None:
            self.manager.fillSyringeTable()
