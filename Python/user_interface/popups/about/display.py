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

from user_interface._custom_widgets.customLabel import BoldLabel

from user_interface._custom_widgets.separators import HorizontalSeparator

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class aboutHelpWindow(qtw.QMainWindow):
    def __init__(self, parent):
        super(aboutHelpWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setWindowModality(qtc.Qt.ApplicationModal)

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle('About...')

        # Show the title
        titleText = BoldLabel(self.parent.title + " - " + self.parent.version)
        self.mainLayout.addWidget(titleText, alignment=qtc.Qt.AlignCenter)

        # Show the date
        dateText = BoldLabel("Release Date: February 2023")
        self.mainLayout.addWidget(dateText)

        self.mainLayout.addWidget(HorizontalSeparator())

        # Show the title
        descText = BoldLabel("Description:")
        self.mainLayout.addWidget(descText)

        # Show the text
        generalText = qtw.QLabel("""MolCommUI is a Python3 software developped by the YanshaLab at King's College London
to control and operate microfluidic Molecular Communication platforms.

More information and documentation can be found on the GitHub page:
https://github.com/""")
        self.mainLayout.addWidget(generalText)#, alignment=qtc.Qt.AlignCenter)

        self.mainLayout.addWidget(HorizontalSeparator())

        # Show the title
        descText = BoldLabel("Contributors and links:")
        self.mainLayout.addWidget(descText)

        # Show the text
        linkText = qtw.QLabel("""Vivien WALTER (walter.vivien@gmail.com)
- Python software
- Arduino software (for syringe pumps)
https://vivien-walter.github.io/

Dadi BI (dadi.bi@kcl.ac.uk)
- Arduino software (for syringe pumps)

The YanshaLab is supervised by Yansha DENG (yansha.deng@kcl.ac.uk)
and based at King's College London
https://www.yanshadeng.org/""")
        self.mainLayout.addWidget(linkText)#, alignment=qtc.Qt.AlignCenter)

        self.mainLayout.addWidget(HorizontalSeparator())

        # Exit button
        self.exitButton = qtw.QPushButton("Close")
        self.exitButton.setFixedWidth(125)
        self.exitButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.exitButton, alignment=qtc.Qt.AlignCenter)

        # Display the panel
        #self.mainLayout.setAlignment(qtc.Qt.AlignCenter)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.resize(300, 300)
        self.show()
        self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['about_help'] = None