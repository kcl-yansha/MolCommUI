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

from user_interface.equipment_config.flow_meter.functions import setFlowMeterFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setFlowMeterWindow(qtw.QMainWindow, setFlowMeterFunctions):
    def __init__(self, parent, flowmeter=None):
        super(setFlowMeterWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setStatusBar(qtw.QStatusBar())

        # Initialise the parameters
        self.active_ports = None
        self.flowmeter = flowmeter
        self.connected = flowmeter is not None
        self.to_load = flowmeter is not None
        self.is_loaded = flowmeter is not None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Set Flow Meter")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createFlowMeterConnectionDisplay(self.mainLayout)
        self.createFlowMeterInfosDisplay(self.mainLayout)
        self.mainLayout.addWidget( HorizontalSeparator() )
        self.createFlowMeterCalibrationDisplay(self.mainLayout)
        self.mainLayout.addWidget( HorizontalSeparator() )
        self.createFlowMeterSettingsDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(550, 400))

        # Initialise the appearance of the button
        self.refreshPIDList()
        self.updateConnectButton()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the port if open
        if self.connected and not self.to_load:
            print('Cancelling connection to '+self.flowmeter.serial_port+'...')
            print('--------------------')

            self.flowmeter.close()

        # Reset the display
        if not self.connected and self.is_loaded:

            # Refresh the information for the files
            self.flowmeter.getFileInfos()

            # Refresh the interfaces
            self.parent.groupDisplay.refreshUI()

        # Close the window
        event.accept()
        self.parent.subWindows['flow_meter'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Generate the display to browse the file
    def createFlowMeterConnectionDisplay(self, parentWidget):

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
        self.refreshButton.setStatusTip("Refresh the list of active ports.")
        self.selectionLayout.addWidget(self.refreshButton, crt_row, 4, 2, 1, alignment=qtc.Qt.AlignBottom)

        crt_row += 1

        # Dropdown for port selection
        self.portComboBox = qtw.QComboBox()
        self.portComboBox.setToolTip("USB port to connect to.")
        self.portComboBox.setStatusTip("USB port to connect to.")
        self.selectionLayout.addWidget(self.portComboBox, crt_row, 0, 1, 4)

        # Populate the list
        self.refreshPortList()

        crt_row += 1

        # Connect button
        self.connectButton = NeutralButton("Connect")
        self.connectButton.clicked.connect(self.connectFlowMeter)
        self.connectButton.setFixedWidth(150)
        self.connectButton.setToolTip('Connect/Disconnect from the selected port')
        self.connectButton.setStatusTip('Connect/Disconnect from the selected port')
        self.selectionLayout.addWidget(self.connectButton, crt_row, 0, 1, 2)

        nameLabel = BoldLabel("Name:")
        self.selectionLayout.addWidget(nameLabel, crt_row, 2, alignment=qtc.Qt.AlignLeft)

        # Add entry for the syringe name
        self.flowMeterName = qtw.QLineEdit()
        self.flowMeterName.setToolTip("Name of the flow meter.")
        self.flowMeterName.setStatusTip("Name of the flow meter.")
        self.selectionLayout.addWidget(self.flowMeterName, crt_row, 3, 1, 2)

        # Display the widget
        self.selectionWidget.setLayout(self.selectionLayout)
        parentWidget.addWidget(self.selectionWidget)

    # -------------------------------------------------
    # Generate the display of the info of the FlowMeter
    def createFlowMeterInfosDisplay(self, parentWidget):

        # Generate the widget
        self.flowMeterInfosWidget = qtw.QWidget()
        self.flowMeterInfosLayout = qtw.QFormLayout(self.flowMeterInfosWidget)

        # Dropdown for equipment type
        self.typeComboBox = AdvComboBox()
        self.typeComboBox.setToolTip("Type of flow meter.")
        self.typeComboBox.setStatusTip("Type of flow meter.")
        self.typeComboBox.addItems( getFlowMeterType() )
        self.typeComboBox.activated.connect(self.setFlowMeter)
        self.flowMeterInfosLayout.addRow(qtw.QLabel('Type:'), self.typeComboBox)

        # Dropdown for equipment type
        self.serialNumberEntry = qtw.QLabel()
        self.serialNumberEntry.setToolTip("Serial Number.")
        self.serialNumberEntry.setStatusTip("Serial Number.")
        self.flowMeterInfosLayout.addRow(qtw.QLabel('S/N:'), self.serialNumberEntry)

        # Display the widget
        self.flowMeterInfosWidget.setLayout(self.flowMeterInfosLayout)
        parentWidget.addWidget(self.flowMeterInfosWidget)

    # ---------------------------------------------------
    # Generate the controls for the flowmeter calibration
    def createFlowMeterCalibrationDisplay(self, parentWidget):

        # Generate the widget
        self.flowMeterCalibrationWidget = qtw.QWidget()
        self.flowMeterCalibrationLayout = qtw.QGridLayout(self.flowMeterCalibrationWidget)

        # Add the spinbox for the delay
        crt_row = 0

        self.flowMeterCalibrationLayout.addWidget( BoldLabel("Calibration"), crt_row, 0, 1, 2 )

        crt_row += 1

        # Add the spinbox for the delay
        self.flowMeterCalibrationLayout.addWidget( qtw.QLabel("Slope:"), crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the spin box
        self.factorSpinBox = qtw.QDoubleSpinBox()
        self.factorSpinBox.setValue(1.0)
        self.factorSpinBox.setMinimum(0.1)
        self.factorSpinBox.setMaximum(100.0)
        self.factorSpinBox.setToolTip("Slope for the calibration of the flow meter")
        self.factorSpinBox.setStatusTip("Slope for the calibration of the flow meter")
        self.flowMeterCalibrationLayout.addWidget(self.factorSpinBox, crt_row, 1 )

        crt_row += 1

        offsetLabel = qtw.QLabel("Offset:")
        self.flowMeterCalibrationLayout.addWidget(offsetLabel, crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the spin box
        self.offsetSpinBox = qtw.QDoubleSpinBox()
        self.offsetSpinBox.setValue(0.0)
        self.offsetSpinBox.setMinimum(-100.0)
        self.offsetSpinBox.setMaximum(100.0)
        self.offsetSpinBox.setToolTip("Offset for the calibration of the flow meter")
        self.offsetSpinBox.setStatusTip("Offset for the calibration of the flow meter")
        self.flowMeterCalibrationLayout.addWidget(self.offsetSpinBox, crt_row, 1 )

        # Display the widget
        self.flowMeterCalibrationWidget.setLayout(self.flowMeterCalibrationLayout)
        parentWidget.addWidget(self.flowMeterCalibrationWidget)

    # --------------------------------------------------
    # Generate the controls for the flowmeter parameters
    def createFlowMeterSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.flowMeterSettingsWidget = qtw.QWidget()
        self.flowMeterSettingsLayout = qtw.QGridLayout(self.flowMeterSettingsWidget)

        crt_row = 0

        # Add the spinbox for the delay
        self.flowMeterSettingsLayout.addWidget( BoldLabel("Delay (ms):"), crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the spin box
        self.delaySpinBox = qtw.QSpinBox()
        self.delaySpinBox.setValue(100)
        self.delaySpinBox.setMinimum(100)
        self.delaySpinBox.setMaximum(5000)
        self.delaySpinBox.setToolTip("Time to wait between two measurement")
        self.delaySpinBox.setStatusTip("Time to wait between two measurement")
        self.flowMeterSettingsLayout.addWidget(self.delaySpinBox, crt_row, 1 )

        crt_row += 1

        PIDLabel = BoldLabel("PID Controller:")
        self.flowMeterSettingsLayout.addWidget(PIDLabel, crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the combo box
        self.PIDControllerComboBox = AdvComboBox()
        #self.PIDControllerComboBox.addItems( getSyringeType(return_list = True) )
        self.PIDControllerComboBox.setToolTip("Selection of the PID controller settings to use with this flow meter")
        self.PIDControllerComboBox.setStatusTip("Selection of the PID controller settings to use with this flow meter")
        self.flowMeterSettingsLayout.addWidget(self.PIDControllerComboBox, crt_row,1 )

        crt_row += 1

        # Add the filter control
        self.createFilterSettingsDisplay(self.flowMeterSettingsLayout, crt_row, 0, 1, 2)

        # Display the widget
        self.flowMeterSettingsWidget.setLayout(self.flowMeterSettingsLayout)
        parentWidget.addWidget(self.flowMeterSettingsWidget)

    # -------------------------------------------
    # Generate the display of the filter settings
    def createFilterSettingsDisplay(self, parentWidget, i_row, i_col, n_rows=1, n_cols=1):

        # Generate the widget
        self.filterSettingsWidget= qtw.QGroupBox('Running average')
        self.filterSettingsWidget.setCheckable(True)
        self.filterSettingsWidget.setChecked(False)
        self.filterSettingsWidget.setToolTip("Enable/Disable a running average filter on the measurement")
        self.filterSettingsWidget.setStatusTip("Enable/Disable a running average filter on the measurement")
        self.filterSettingsLayout = qtw.QFormLayout(self.filterSettingsWidget)

        # Add the spin box
        self.filterValueSpinBox = qtw.QSpinBox()
        self.filterValueSpinBox.setMinimum(2)
        self.filterValueSpinBox.setMaximum(1000)
        self.filterValueSpinBox.setValue(10)
        self.filterValueSpinBox.setToolTip("Window size to use for a running average filter")
        self.filterValueSpinBox.setStatusTip("Window size to use for a running average filter")
        self.filterSettingsLayout.addRow('Window size:', self.filterValueSpinBox)

        # Display the widget
        self.filterSettingsWidget.setLayout(self.filterSettingsLayout)
        parentWidget.addWidget(self.filterSettingsWidget, i_row, i_col, n_rows, n_cols)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.setButton = AcceptButton("Set")
        self.setButton.clicked.connect(self.saveFlowMeter)
        self.setButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.setButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
