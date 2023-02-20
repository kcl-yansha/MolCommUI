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

import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from settings.equipment.syringe_settings import getSyringeList, saveSyringeGroupConfig, saveSyringeGroupFile

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class saveSyringePumpSettingsFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # -----------------------------------------------------------
    # Update the status of the Browse bar depending on the status
    def updateBrowseStatus(self):
        self.fileBrowsing.setEnabled( self.fileCheckbox.isChecked() )

    ##-\-\-\-\-\-\-\-\
    ## PATH MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # --------------------------
    # Open the connection window
    def browsePath(self):

        # Get the initial text
        filename = self.nameEntry.text()
        filepath = os.path.join(self.parent.current_folder, filename)

        # Browse for the file setting
        settingFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Settings...", filepath, "Setting File (*.ini)")

        # Process
        if settingFile != "":

            # Update the selected folder
            self.parent.current_folder = os.path.dirname(settingFile)

            # Apply the change
            self.fileBrowsing.setText(settingFile)

    ##-\-\-\-\-\
    ## SAVE FILES
    ##-/-/-/-/-/

    # -----------------
    # Save the settings
    def saveSelectionSettings(self):

        # Get the name to use for save
        config_name = self.nameEntry.text()

        # Check if the name is free
        object_list = getSyringeList(self.parent.main_config['current_user'], object_type='group')
        pumps_list = getSyringeList(self.parent.main_config['current_user'])
        object_list = object_list + pumps_list

        # Raise an issue if no selection
        if not self.settingsCheckbox.isChecked() and not self.fileCheckbox.isChecked():
            errorMessage("Selection Error","Select at least one destination to save the parameters in.")
            return 0

        # Get the config for the syringe group
        config_dict = self.syringe_group.syringes[ self.axis ].getSettings()

        # Save in the local config file
        if self.settingsCheckbox.isChecked():

            # Raise an issue if the name exist
            if config_name in object_list:
                errorMessage("Invalid Name", config_name + " is already used as a config name.")
                return 0

            # Save the config
            saveSyringeGroupConfig(config_name, config_dict, self.parent.main_config['current_user'])

        # Save in a config file
        if self.fileCheckbox.isChecked():

            # Raise an issue if a path hasn't been given
            if self.fileBrowsing.text() == "":
                errorMessage("Missing Path", "You need to select a path to save in file.")
                return 0

            # Get the path
            config_path = self.fileBrowsing.text()

            # Save the config
            saveSyringeGroupFile(config_name, config_dict, config_path)

        # Close the window
        self.close()
