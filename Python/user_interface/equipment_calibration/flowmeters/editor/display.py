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

from equipment.flow_meter.properties import getFlowMeterType

from user_interface._custom_widgets.buttons import NeutralButton, AcceptButton, CancelButton
from user_interface._custom_widgets.comboboxes import AdvComboBox
from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.separators import HorizontalSeparator, VerticalSeparator

from user_interface.equipment_calibration.flowmeters.editor.functions import editFlowmeterCalibrationFunction

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class editFlowmeterCalibrationWindow(qtw.QMainWindow, editFlowmeterCalibrationFunction):
    def __init__(self, parent, calibration_manager=None, flowmeter_serial=None):
        super(editFlowmeterCalibrationWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.manager = calibration_manager

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Edit Flowmeter")
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
        #self.setFixedSize(qtc.QSize(400, 300))

        # Initialise the window
        self.initialiseWindow(flowmeter_serial=flowmeter_serial)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['edit_flowmeter'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------
    # Generate the name controller
    def createNameDisplay(self, parentWidget):

        # Generate the widget
        self.selectionWidget = qtw.QWidget()
        self.selectionLayout = qtw.QGridLayout(self.selectionWidget)

        crt_row = 0

        # Text
        boxLabel = BoldLabel("USB Port:")
        self.selectionLayout.addWidget(boxLabel, crt_row, 0, 1, 5)

        # Refresh button
        self.refreshButton = IconButton(icon_size=25, icon='refresh_button.png')
        self.refreshButton.released.connect(self.refreshPortList)
        self.refreshButton.setToolTip("Refresh the list of active ports.")
        self.selectionLayout.addWidget(self.refreshButton, crt_row, 4, 2, 1, alignment=qtc.Qt.AlignBottom)

        crt_row += 1

        # Dropdown for port selection
        self.portComboBox = qtw.QComboBox()
        self.portComboBox.setToolTip("USB port to connect to.")
        self.selectionLayout.addWidget(self.portComboBox, crt_row, 0, 1, 4)

        # Populate the list
        self.refreshPortList()

        crt_row += 1

        # Connect button
        self.connectButton = NeutralButton("Check")
        self.connectButton.clicked.connect(self.checkFlowMeter)
        self.connectButton.setFixedWidth(100)
        self.selectionLayout.addWidget(self.connectButton, crt_row, 0, 1, 2)

        nameLabel = BoldLabel("Serial Number:")
        self.selectionLayout.addWidget(nameLabel, crt_row, 2, alignment=qtc.Qt.AlignLeft)

        # Add entry for the syringe name
        self.flowMeterName = qtw.QLineEdit()
        self.flowMeterName.setToolTip("Serial number of the flow meter to use.")
        self.selectionLayout.addWidget(self.flowMeterName, crt_row, 3, 1, 2)

        # Display the widget
        self.selectionWidget.setLayout(self.selectionLayout)
        parentWidget.addWidget(self.selectionWidget)

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

        # Add volume
        self.typeComboBox = AdvComboBox()
        self.typeComboBox.setToolTip("Type of flow meter.")
        self.typeComboBox.addItems( getFlowMeterType() )
        self.settingsLayout.addRow('Type:', self.typeComboBox)

        # Add calibration factor
        self.calibrationEntry = qtw.QLineEdit()
        self.settingsLayout.addRow('Calibration factor', self.calibrationEntry)

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
