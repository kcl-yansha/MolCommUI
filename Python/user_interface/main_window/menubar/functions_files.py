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

from settings.user import getUserList, createNewUser

from user_interface._common_functions.window_handling import openWindow
from user_interface.popups.notifications import errorMessage
from user_interface.popups.experiment_config.display import setExperimentWindow
from user_interface.popups.user_settings.display import userSettingsWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarFilesFunctions(object):

    ##-\-\-\-\-\-\
    ## Window MENU
    ##-/-/-/-/-/-/

    # ------------------------------
    # Open the new experiment window
    def callNewExperiment(self):
        openWindow(self.parent, setExperimentWindow, 'experiment')

    # ------------------------------
    # Open the current experiment window
    def callEditExperiment(self):
        openWindow(self.parent, setExperimentWindow, 'experiment', experiment=self.parent.experiment)

    # -------------------------------
    # Select the user for the session
    def callUserSelection(self):

        # Get the list of users
        all_users = getUserList()

        # Get the current user
        crt_user = self.parent.main_config['current_user']
        crt_ID = all_users.index(crt_user)

        # Prompt the user
        new_user, ok = qtw.QInputDialog.getItem(self.parent, 'Load User', 'Select the user profile to load', all_users, crt_ID, False)

        # Modify if required
        if ok:

            # Select the new user
            self.parent.main_config['current_user'] = new_user
            self.parent.loadUser()

    # ------------------------
    # Open the new user window
    def callNewUser(self):

        # Prompt the user
        new_user, ok = qtw.QInputDialog.getText(self.parent, 'New Username', 'Create a new user profile', qtw.QLineEdit.Normal, 'New user')

        # Modify if required
        if ok:

            # Check for forbidden values
            if new_user.upper() == 'DEFAULT':
                errorMessage('Invalid Name',new_user+ ' is not a valid username.')

            # Check if already exists
            elif new_user.upper() in [x.upper() for x in getUserList()]:
                errorMessage('Invalid Name',new_user+ ' is an existing username.')

            else:
                # Create the new user
                createNewUser(new_user)

                # Select the new user
                self.parent.main_config['current_user'] = new_user
                self.parent.loadUser()

                # Edit the new user settings
                openWindow(self.parent, userSettingsWindow, 'user_settings')
