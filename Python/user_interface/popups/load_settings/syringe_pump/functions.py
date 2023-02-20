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

from settings.equipment.syringe_settings import getSyringeList, loadSyringeGroupConfig, loadSyringeGroupFile

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class loadSyringePumpSettingsFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # ------------------------------------------------------------
    # Update the status of the Combobox depending on the selection
    def updateComboboxSelection(self):

        # Get the list
        object_list = getSyringeList(self.parent.main_config['current_user'])

        # Empty the combo box
        self.syringeSettingsComboBox.clear()

        # Update the combo box
        self.syringeSettingsComboBox.addItems( object_list )

    ##-\-\-\-\-\-\-\-\
    ## PATH MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # --------------------------
    # Open the connection window
    def browsePath(self):

        # Browse for the file setting
        settingFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Load Settings...", self.parent.current_folder, "Setting File (*.ini)")

        # Process
        if settingFile != "":

            # Update the selected folder
            self.parent.current_folder = os.path.dirname(settingFile)

            # Apply the change
            self.fileBrowsing.setText(settingFile)

    ##-\-\-\-\-\
    ## LOAD FILES
    ##-/-/-/-/-/

    # ------------------
    # Load the selection
    def loadSelection(self):

        # Retrieve the local selection
        if self.syringeTabWidget.currentIndex() == 0:
            syringe_config = loadSyringeGroupConfig(self.syringeSettingsComboBox.currentText(), self.parent.main_config['current_user'] )

        # Read the selected file
        else:
            if self.fileBrowsing.text() != "":
                syringe_config = loadSyringeGroupFile( self.fileBrowsing.text() )

            # Raise an error if no file has been selected
            else:
                errorMessage('No selection', 'No setting file has been selected.')
                return 0

            # Raise an error if the config is not for a single pump
            if syringe_config['type'] == 'group':
                errorMessage('Selection error', 'The selected file is for a syringe group. Please select a file for a single syringe pump.')
                return 0

        # Update the config
        self.syringe_group.syringes[self.axis].loadSettings(syringe_config)

        print('Load syringe pump settings ' + syringe_config['name'])
        print('--------------------')

        # Update the properties
        self.interface.updateProperties()

        # Close the window
        self.close()
