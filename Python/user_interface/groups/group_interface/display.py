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

from user_interface._common_functions.path_to_assets import getIcon

from user_interface.groups.group_interface.functions import EquipmentGroupsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class EquipmentGroups(qtw.QScrollArea, EquipmentGroupsFunctions):
    def __init__(self, parent):
        super(EquipmentGroups, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.groups = []
        self.groups_widget = []

        # Edit the property of the widget
        self.setWidgetResizable(True)

        # Initialise the widget
        self.content = qtw.QWidget(self)
        self.layout = qtw.QVBoxLayout(self.content)

        # Accept drag and drop events
        self.setAcceptDrops(True)

        # Display the widget
        self.content.setLayout(self.layout)
        self.setWidget(self.content)
