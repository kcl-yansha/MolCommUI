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

##-\-\-\-\-\-\-\-\-\-\-\-\
## LABEL WITH SPECIFIC TEXT
##-/-/-/-/-/-/-/-/-/-/-/-/

# ---------------------
# Generate a bold label
class BoldLabel(qtw.QLabel):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QLabel.__init__(self, *args, **kwargs)

        # Set the bold text
        font = qtg.QFont()
        font.setBold(True)
        self.setFont(font)

# ------------------------
# Generate an italic label
class ItalicLabel(qtw.QLabel):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QLabel.__init__(self, *args, **kwargs)

        # Set the bold text
        font = qtg.QFont()
        font.setItalic(True)
        self.setFont(font)
