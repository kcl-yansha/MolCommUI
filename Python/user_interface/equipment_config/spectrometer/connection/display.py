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

from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.comboboxes import AdvComboBox
from user_interface._custom_widgets.buttons import NeutralButton, AcceptButton, CancelButton
from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.separators import HorizontalSeparator, VerticalSeparator

from user_interface.equipment_config.spectrometer.connection.functions import setSpectroMeterFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setSpectroMeterWindow(qtw.QMainWindow, setSpectroMeterFunctions):
    def __init__(self, parent, spectrometer=None):
        super(setSpectroMeterWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setStatusBar(qtw.QStatusBar())

        # Initialise the parameters
        self.active_ports = None
        self.spectrometer = spectrometer
        self.connected = spectrometer is not None
        self.to_load = spectrometer is not None
        self.is_loaded = spectrometer is not None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Set Spectrometer")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createSpectroMeterConnectionDisplay(self.mainLayout)
        self.createSpectroMeterSettingsDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(550, 400))

        # Initialise the appearance of the button
        self.refreshPortList()
        self.updateConnectButton()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the port if open
        if self.connected and not self.to_load:
            print('Cancelling connection to '+self.spectrometer.serial_number+'...')
            print('--------------------')

            self.spectrometer.close()

        # Reset the display
        if not self.connected and self.is_loaded:
            self.parent.groupDisplay.refreshUI()

        # Close the window
        event.accept()
        self.parent.subWindows['spectrometer'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Generate the display to browse the file
    def createSpectroMeterConnectionDisplay(self, parentWidget):

        # Generate the widget
        self.selectionWidget = qtw.QWidget()
        self.selectionLayout = qtw.QGridLayout(self.selectionWidget)

        crt_row = 0

        # Text
        boxLabel = BoldLabel("Detected Spectrometer:")
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
        self.portComboBox.setToolTip("Spectrometer to connect to.")
        self.portComboBox.setStatusTip("Spectrometer to connect to.")
        self.selectionLayout.addWidget(self.portComboBox, crt_row, 0, 1, 4)

        crt_row += 1

        # Connect button
        self.connectButton = NeutralButton("Connect")
        self.connectButton.clicked.connect(self.connectSpectrometer)
        self.connectButton.setFixedWidth(150)
        self.connectButton.setToolTip('Connect/Disconnect from the selected port')
        self.connectButton.setStatusTip('Connect/Disconnect from the selected port')
        self.selectionLayout.addWidget(self.connectButton, crt_row, 0, 1, 2)

        nameLabel = BoldLabel("Name:")
        self.selectionLayout.addWidget(nameLabel, crt_row, 2, alignment=qtc.Qt.AlignLeft)

        # Add entry for the syringe name
        self.spectroMeterName = qtw.QLineEdit()
        self.spectroMeterName.setToolTip("Name of the spectrometer.")
        self.spectroMeterName.setStatusTip("Name of the spectrometer.")
        self.selectionLayout.addWidget(self.spectroMeterName, crt_row, 3, 1, 2)

        # Display the widget
        self.selectionWidget.setLayout(self.selectionLayout)
        parentWidget.addWidget(self.selectionWidget)

    # -----------------------------------------------------
    # Generate the controls for the spectrometer parameters
    def createSpectroMeterSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.spectroMeterSettingsWidget = qtw.QWidget()
        self.spectroMeterSettingsLayout = qtw.QGridLayout(self.spectroMeterSettingsWidget)

        crt_row = 0

        # Model
        self.spectroMeterModel = qtw.QLabel('Model:')
        self.spectroMeterSettingsLayout.addWidget(self.spectroMeterModel, crt_row, 0 )

        # Pixels
        self.spectroMeterPixels = qtw.QLabel('Pixels:')
        self.spectroMeterSettingsLayout.addWidget(self.spectroMeterPixels, crt_row, 1 )

        crt_row += 1

        # Add the spinbox for the delay
        self.spectroMeterSettingsLayout.addWidget( BoldLabel("Integration Time (ms):"), crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the spin box
        self.integrationSpinBox = qtw.QSpinBox()
        self.integrationSpinBox.setMinimum(100)
        self.integrationSpinBox.setMaximum(60000)
        self.integrationSpinBox.setValue(100)
        self.integrationSpinBox.setToolTip("Integration time to use with the spectrometer.")
        self.integrationSpinBox.setStatusTip("Integration time to use with the spectrometer.")
        self.spectroMeterSettingsLayout.addWidget(self.integrationSpinBox, crt_row, 1 )

        crt_row += 1

        # Add the spinbox for the delay
        self.spectroMeterSettingsLayout.addWidget( BoldLabel("Sampling Rate (ms):"), crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the spin box
        self.delaySpinBox = qtw.QSpinBox()
        self.delaySpinBox.setMinimum(100)
        self.delaySpinBox.setMaximum(60000)
        self.delaySpinBox.setValue(100)
        self.delaySpinBox.setToolTip("Sampling rate to use with the spectrometer. Should be higher than the integration time.")
        self.delaySpinBox.setStatusTip("Sampling rate to use with the spectrometer. Should be higher than the integration time.")
        self.spectroMeterSettingsLayout.addWidget(self.delaySpinBox, crt_row, 1 )

        # Display the widget
        self.spectroMeterSettingsWidget.setLayout(self.spectroMeterSettingsLayout)
        parentWidget.addWidget(self.spectroMeterSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.setButton = AcceptButton("Set")
        self.setButton.clicked.connect(self.saveSpectroMeter)
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
