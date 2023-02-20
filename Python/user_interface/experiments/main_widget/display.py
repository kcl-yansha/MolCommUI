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

from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.separators import VerticalSeparator

from user_interface.experiments.main_widget.functions import experimentDisplayFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class experimentDisplay(qtw.QWidget, experimentDisplayFunctions):
    def __init__(self, parent):
        super(experimentDisplay, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Initialise the widget
        self.layout = qtw.QHBoxLayout(self)

        # Experiment name
        self.experimentName = qtw.QLabel('Experiment: New Experiment')
        self.layout.addWidget(self.experimentName)

        # Separator
        separator = BoldLabel('|')
        separator.setFixedWidth(5)
        self.layout.addWidget(separator, alignment=qtc.Qt.AlignCenter)

        # Experiment status
        self.experimentStatus = qtw.QLabel('Status: Recording')
        self.layout.addWidget(self.experimentStatus)

        # Display the widget
        self.setLayout(self.layout)
