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

##-\-\-\-\-\-\-\-\-\-\-\
## CALL WINDOW FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/-/

# -------------------------------------
# Check if the window is already opened
def _is_window_open(parent, window_tag):

    # Initialise if it does not exist
    if window_tag not in parent.subWindows.keys():
        parent.subWindows[window_tag] = None

    return parent.subWindows[window_tag] is None

# ---------------
# Open the window
def openWindow(parent, window_class, window_tag, **kwargs):

    # Check if the window is not open yet
    if _is_window_open(parent, window_tag):
        parent.subWindows[window_tag] = window_class(parent, **kwargs)
    else:
        parent.subWindows[window_tag].raise_()
        parent.subWindows[window_tag].activateWindow()
