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
from user_interface._custom_widgets.buttons import NeutralButton, CancelButton
from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.separators import HorizontalSeparator, VerticalSeparator
from user_interface._custom_widgets.table import CTableWidget

from user_interface.equipment_calibration.syringes.manager.functions import calibrateSyringeFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class calibrateSyringeWindow(qtw.QMainWindow, calibrateSyringeFunctions):
    def __init__(self, parent):
        super(calibrateSyringeWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Calibrate Syringes")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createTableWidget(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(qtc.QSize(425, 300))

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['calibrate_syringe'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------------
    # Generate the table display for the trackers
    def createTableWidget(self, parentWidget):

        # Generate the widget
        self.syringeCalibrationWidget = qtw.QWidget()
        self.syringeCalibrationLayout = qtw.QVBoxLayout(self.syringeCalibrationWidget)

        # Generate the table of servers
        self.syringeTable = CTableWidget(0, 6)
        self.syringeTable.setLabels( ['Name', '', '', 'Volume', 'Diameter', 'Calibration'] )

        self.syringeTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.syringeTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        self.syringeTable.setShowGrid(False)
        self.syringeTable.setMinimumHeight(100)
        self.syringeCalibrationLayout.addWidget(self.syringeTable)

        # Populate the widget
        self.fillSyringeTable()

        # Display the widget
        self.syringeCalibrationWidget.setLayout(self.syringeCalibrationLayout)
        parentWidget.addWidget(self.syringeCalibrationWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.newButton = NeutralButton("New")
        self.newButton.clicked.connect(lambda x:self.editSyringe(None))
        self.newButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.newButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
