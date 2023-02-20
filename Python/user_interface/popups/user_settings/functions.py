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

from settings.equipment.reload_equipment import togglePreload

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class userSettingsFunctions(object):

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------------
    # Browse for the default folder to use
    def browseDefaultFolder(self):

        # Get the current folder
        current_folder = self.defaultFolderBrowser.text()

        # Browse for the file setting
        defaultFolder = qtw.QFileDialog.getExistingDirectory(self.parent, "Select Default Folder", current_folder, qtw.QFileDialog.ShowDirsOnly)

        # Process
        if defaultFolder != "":

            # Update the last selected folder
            self.parent.current_folder = defaultFolder

            # Apply the change
            self.defaultFolderBrowser.setText(defaultFolder)

    # ---------------------
    # Apply all the changes
    def saveUserSettings(self):

        # Update the user settings - General
        self.parent.editConfig( 'save_folder', self.defaultFolderBrowser.text() )
        self.parent.editConfig( 'use_date', self.datedFolderCheckbox.isChecked() )

        togglePreload(self.loadEquipmentCheckbox.isChecked(), user_name=self.parent.main_config['current_user'] )

        # Close the windows
        self.close()
