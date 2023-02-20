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

from settings.equipment.gearbox_calibration import getDefaultCalibration, getGearboxesList, saveGearboxConfig, loadGearboxCalibrationConfig

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class editGearboxCalibrationFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # ---------------------
    # Initialise the window
    def initialiseWindow(self, gearbox_name=None):

        # Set default for a new syringe
        if gearbox_name is None:

            # Edit the name
            self.nameEntry.setText('New gearbox')
            self.check_name = True

            # Load the values
            calibration_dict = getDefaultCalibration()

        else:

            # Edit the name
            self.nameEntry.setText(gearbox_name)
            self.nameEntry.setDisabled(True)
            self.check_name = False

            # Load the values
            calibration_dict = loadGearboxCalibrationConfig(gearbox_name)

        # Edit the window content
        self.ratioEntry.setValue(calibration_dict['ratio'])
        self.calibrationEntry.setText( str(calibration_dict['calibration_factor']) )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------
    # Save the settings
    def saveSettings(self):

        # Get the values
        gearbox_name = self.nameEntry.text()
        gearbox_dict = {
        # General
        'ratio':self.ratioEntry.value(),
        # Settings
        'calibration_factor':float( self.calibrationEntry.text() ),
        }

        # Check that the name if accepted
        if self.check_name:

            # Get the list of names in the memory
            all_names = getGearboxesList()

            # Raise an issue if the name exist
            if gearbox_name.lower() == 'default':
                errorMessage("Invalid Name", "Default cannot be used as a gearbox name.")
                return 0

            # Raise an issue if the name exist
            if gearbox_name in all_names:
                errorMessage("Invalid Name", gearbox_name + " is already used as a gearbox name.")
                return 0

        # Save the value in file
        saveGearboxConfig(gearbox_name, gearbox_dict)

        # Apply the change
        for opened_syringe in self.parent.equipments['syringe_pumps']:
            #opened_syringe.equipment.updateSyringeType()
            pass

        # Close the window
        self.close()

        # Reload the parent window
        if self.manager is not None:
            self.manager.fillGearboxTable()
