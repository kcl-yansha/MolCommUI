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

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.user_settings.display import userSettingsWindow
from user_interface.popups.debug_settings.display import debugSettingsWindow
from user_interface.popups.about.display import aboutHelpWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarHelpFunctions(object):

    ##-\-\-\-\-\-\
    ## Window MENU
    ##-/-/-/-/-/-/

    # -----------------------------
    # Open the user settings window
    def callUserSettingsWindow(self):
        openWindow(self.parent, userSettingsWindow, 'user_settings')

    # -----------------------------
    # Open the user settings window
    def callDebugSettingsWindow(self):
        openWindow(self.parent, debugSettingsWindow, 'debug_settings')

    # ---------------------
    # Open the about window
    def callAboutWindow(self):
        openWindow(self.parent, aboutHelpWindow, 'about_help')
