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

from user_interface.equipment_config.spectrometer.edit.functions import editSpectroMeterFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class editSpectroMeterWindow(qtw.QMainWindow, editSpectroMeterFunctions):
    def __init__(self, parent, spectrometer=None):
        super(editSpectroMeterWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setStatusBar(qtw.QStatusBar())

        # Initialise the parameters
        self.spectrometer = spectrometer

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Edit Spectrometer")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createSpectroMeterSettingsDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(550, 400))

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['spectrometer'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------------
    # Generate the controls for the spectrometer parameters
    def createSpectroMeterSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.spectroMeterSettingsWidget = qtw.QWidget()
        self.spectroMeterSettingsLayout = qtw.QGridLayout(self.spectroMeterSettingsWidget)

        crt_row = 0

        # Name
        nameLabel = BoldLabel("Name:")
        self.spectroMeterSettingsLayout.addWidget(nameLabel, crt_row, 0, alignment=qtc.Qt.AlignLeft)

        # Add entry for the syringe name
        self.spectroMeterName = qtw.QLineEdit()
        self.spectroMeterName.setText(self.spectrometer.name)
        self.spectroMeterName.setToolTip("Name of the spectrometer.")
        self.spectroMeterName.setStatusTip("Name of the spectrometer.")
        self.spectroMeterSettingsLayout.addWidget(self.spectroMeterName, crt_row, 1)

        crt_row += 1

        # Model
        self.spectroMeterModel = qtw.QLabel('Model:')
        self.spectroMeterModel.setText( 'Model: ' + self.spectrometer.model )
        self.spectroMeterSettingsLayout.addWidget(self.spectroMeterModel, crt_row, 0 )

        # Pixels
        self.spectroMeterPixels = qtw.QLabel('Pixels:')
        self.spectroMeterPixels.setText( 'Pixels: ' + str(self.spectrometer.n_pixels) )
        self.spectroMeterSettingsLayout.addWidget(self.spectroMeterPixels, crt_row, 1 )

        crt_row += 1

        # Add the spinbox for the delay
        self.spectroMeterSettingsLayout.addWidget( BoldLabel("Integration Time (ms):"), crt_row, 0, alignment=qtc.Qt.AlignRight )

        # Add the spin box
        self.integrationSpinBox = qtw.QSpinBox()
        self.integrationSpinBox.setMinimum(100)
        self.integrationSpinBox.setMaximum(60000)
        self.integrationSpinBox.setValue(self.spectrometer.integration_time)
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
        self.delaySpinBox.setValue(self.spectrometer.delay_time)
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
        self.setButton = AcceptButton("Save")
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
