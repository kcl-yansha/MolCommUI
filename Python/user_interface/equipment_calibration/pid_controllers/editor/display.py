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

from user_interface.equipment_calibration.pid_controllers.editor.functions import editPIDCalibrationFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class editPIDCalibrationWindow(qtw.QMainWindow, editPIDCalibrationFunctions):
    def __init__(self, parent, calibration_manager=None, controller_name=None):
        super(editPIDCalibrationWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.manager = calibration_manager

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Edit PID Controller")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createNameDisplay(self.mainLayout)
        self.mainLayout.addWidget( HorizontalSeparator() )
        self.createCalibrationDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(qtc.QSize(400, 300))

        # Initialise the window
        self.initialiseWindow(controller_name=controller_name)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['edit_pid'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------
    # Generate the name controller
    def createNameDisplay(self, parentWidget):

        # Generate the widget
        self.setNameWidget = qtw.QWidget()
        self.setNameLayout = qtw.QHBoxLayout(self.setNameWidget)

        # Display the name
        self.setNameLayout.addWidget( BoldLabel("Name:") )

        self.nameEntry = qtw.QLineEdit()
        self.setNameLayout.addWidget( self.nameEntry )

        # Display the widget
        self.setNameWidget.setLayout(self.setNameLayout)
        parentWidget.addWidget(self.setNameWidget)

    # ---------------------------------------------
    # Make the widget and layout to contain the tab
    def initTab(self):

        # Initialise
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout(widget)

        # Display
        widget.setLayout(layout)

        return widget, layout

    # ------------------------------------
    # Generate the calibration tab display
    def createCalibrationDisplay(self, parentWidget):

        # Generate the widget
        self.calibrationTabWidget = qtw.QTabWidget()

        # Add the first tab - Settings
        self.propertiesWidget, self.propertiesLayout = self.initTab()
        self.createSettingsDisplay(self.propertiesLayout)
        self.calibrationTabWidget.addTab(self.propertiesWidget, 'Settings')

        # Display the widget
        parentWidget.addWidget(self.calibrationTabWidget)

    # --------------------------------
    # Generate the settings controller
    def createSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.settingsWidget = qtw.QWidget()
        self.settingsLayout = qtw.QFormLayout(self.settingsWidget)

        # Add value for proportional
        self.pValueEntry = qtw.QDoubleSpinBox()
        self.pValueEntry.setMinimum(-1000)
        self.pValueEntry.setDecimals(5)
        self.pValueEntry.setMaximum(1000)
        self.settingsLayout.addRow('P coefficient:', self.pValueEntry)

        # Add value for integration
        self.iValueEntry = qtw.QDoubleSpinBox()
        self.iValueEntry.setMinimum(-1000)
        self.iValueEntry.setDecimals(5)
        self.iValueEntry.setMaximum(1000)
        self.settingsLayout.addRow('I coefficient:', self.iValueEntry)

        # Add value for differentiate
        self.dValueEntry = qtw.QDoubleSpinBox()
        self.dValueEntry.setMinimum(-1000)
        self.dValueEntry.setDecimals(5)
        self.dValueEntry.setMaximum(1000)
        self.settingsLayout.addRow('D coefficient:', self.dValueEntry)

        # Display the widget
        self.settingsWidget.setLayout(self.settingsLayout)
        parentWidget.addWidget(self.settingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = AcceptButton("Save")
        self.saveButton.clicked.connect(self.saveSettings)
        self.saveButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.saveButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
