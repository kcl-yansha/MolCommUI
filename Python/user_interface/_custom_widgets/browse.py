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

import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

# -------------------------------------------------------------------------------
# Generate a QLineEdit and a QButton (with a QLabel if requested) to browse files
class Browse(qtw.QWidget):
    def __init__(self, label=None, bold=True, read_only=True):
        super(Browse, self).__init__()

        # User name entry
        self.layout = qtw.QHBoxLayout( self )

        # Add the label on the left
        if label is not None:
            if bold:
                self.label = CLabel(label)
            else:
                self.label = QLabel(label)
            self.layout.addWidget(self.label)

        # Add the QLineEdit widget
        self.lineEdit = qtw.QLineEdit()
        self.layout.addWidget(self.lineEdit)

        if read_only:
            self.lineEdit.setReadOnly(True)

        # Add the browse button
        self.pushButton = qtw.QPushButton('Browse')
        self.pushButton.setFixedWidth(100)
        self.layout.addWidget(self.pushButton)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Change the disabled status (1)
    def setEnabled(self, status):
        self.lineEdit.setEnabled(status)
        self.pushButton.setEnabled(status)

    # ------------------------------
    # Change the disabled status (1)
    def setDisabled(self, status):
        self.lineEdit.setDisabled(status)
        self.pushButton.setDisabled(status)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## ACCESS THE LINEEDIT WIDGET
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Get the text from the Line Edit widget
    def text(self):
        return self.lineEdit.text()

    # ------------------------------------
    # Edit the text in the LineEdit widget
    def setText(self, new_text):
        self.lineEdit.setText(new_text)

    ##-\-\-\-\
    ## CONNECT
    ##-/-/-/-/

    # --------------------------------
    # Connect the action to the button
    def connectButton(self, connected_function):
        self.pushButton.clicked.connect(connected_function)

    # ---------------------------------------
    # Connect the entry control to a function
    def connectEntry(self, connected_function):
        self.pushButton.editingFinished.connect(connected_function)

    # ------------------------------------------
    # Connect both controls to the same function
    def connect(self, connected_function):
        self.connectButton(connected_function)
        self.connectEntry(connected_function)
