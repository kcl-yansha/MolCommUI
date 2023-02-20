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
from user_interface._custom_widgets.buttons import AcceptButton, CancelButton
from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.separators import HorizontalSeparator, VerticalSeparator

from user_interface.scheduler.assign_pumps.functions import assignPumpFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class assignPumpWindow(qtw.QDialog, assignPumpFunctions):
    def __init__(self, pump_names, parent=None):
        super(assignPumpWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.pump_names = pump_names
        self.pump_dict = None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Assign Pumps")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createPumpSelection(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.setLayout(self.mainLayout)
        #self.setFixedSize(qtc.QSize(425, 300))

        # Initialise the display
        self.populatePumpList()

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the controls for the user
    def createPumpSelection(self, parentWidget):

        # Generate the widget
        self.pumpSelectionWidget = qtw.QWidget()
        self.pumpSelectionLayout = qtw.QFormLayout(self.pumpSelectionWidget)

        # Display the widget
        self.pumpSelectionWidget.setLayout(self.pumpSelectionLayout)
        parentWidget.addWidget(self.pumpSelectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.newButton = AcceptButton("Set")
        self.newButton.clicked.connect(self.setPulse)
        self.newButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.newButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
