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

##-\-\-\-\-\-\-\-\
## COLOURED BUTTONS
##-/-/-/-/-/-/-/-/

# -------------------------
# Button with neutral color
class NeutralButton(qtw.QPushButton):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QPushButton.__init__(self, *args, **kwargs)

    ##-\-\-\-\
    ## METHODS
    ##-/-/-/-/
    def setColor(self, color):

        # Get the button palette
        palette = self.palette()
        role = self.backgroundRole()

        # Change the palette
        palette.setColor(role, qtg.QColor(color))
        self.setPalette(palette)

# ------------------------
# Button to confirm action
class AcceptButton(qtw.QPushButton):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QPushButton.__init__(self, *args, **kwargs)

        # Set the bold text
        self.setStyleSheet("background-color: #247E5C")

# -----------------------
# Button to cancel action
class CancelButton(qtw.QPushButton):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QPushButton.__init__(self, *args, **kwargs)

        # Set the bold text
        self.setStyleSheet("background-color: #8C2E2E")

# -----------------
# Button to connect
class ConnectionButton(qtw.QPushButton):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QPushButton.__init__(self, *args, **kwargs)

        # Set the bold text
        self.setStyleSheet("background-color: #2d6f8b")
