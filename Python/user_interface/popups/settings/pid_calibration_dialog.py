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

from user_interface._custom_widgets.separators import HorizontalSeparator

##-\-\-\-\-\-\-\-\-\-\
## DIALOG FOR SETTINGS
##-/-/-/-/-/-/-/-/-/-/

class PIDCalibrationSettings(qtw.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the title
        self.setWindowTitle("Calibration settings")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Initialise parameters
        self.settings = {}

        # Make the display
        self.layout = qtw.QFormLayout()

        # Get the controls
        self.lowFlowSpinbox = qtw.QDoubleSpinBox()
        self.lowFlowSpinbox.setMinimum(0)
        self.lowFlowSpinbox.setDecimals(2)
        self.lowFlowSpinbox.setMaximum(1000)
        self.lowFlowSpinbox.setValue( parent.low_flowrate )
        self.layout.addRow('Low Flowrate (uL/min):', self.lowFlowSpinbox)

        self.lowTimeSpinbox = qtw.QDoubleSpinBox()
        self.lowTimeSpinbox.setMinimum(0)
        self.lowTimeSpinbox.setDecimals(2)
        self.lowTimeSpinbox.setMaximum(60)
        self.lowTimeSpinbox.setValue( parent.low_time )
        self.layout.addRow('Low Time (min):', self.lowTimeSpinbox)

        self.highFlowSpinbox = qtw.QDoubleSpinBox()
        self.highFlowSpinbox.setMinimum(0)
        self.highFlowSpinbox.setDecimals(2)
        self.highFlowSpinbox.setMaximum(1000)
        self.highFlowSpinbox.setValue( parent.high_flowrate )
        self.layout.addRow('High Flowrate (uL/min):', self.highFlowSpinbox)

        self.highTimeSpinbox = qtw.QDoubleSpinBox()
        self.highTimeSpinbox.setMinimum(0)
        self.highTimeSpinbox.setDecimals(2)
        self.highTimeSpinbox.setMaximum(60)
        self.highTimeSpinbox.setValue( parent.high_time )
        self.layout.addRow('High Time (min):', self.highTimeSpinbox)

        self.layout.addRow(HorizontalSeparator())

        self.measureStartSpinbox = qtw.QDoubleSpinBox()
        self.measureStartSpinbox.setMinimum(0)
        self.measureStartSpinbox.setDecimals(2)
        self.measureStartSpinbox.setMaximum(60)
        self.measureStartSpinbox.setValue( parent.measure_range[0] )
        self.layout.addRow('Start meas. (min):', self.measureStartSpinbox)

        self.measureStopSpinbox = qtw.QDoubleSpinBox()
        self.measureStopSpinbox.setMinimum(0)
        self.measureStopSpinbox.setDecimals(2)
        self.measureStopSpinbox.setMaximum(60)
        self.measureStopSpinbox.setValue( parent.measure_range[1] )
        self.layout.addRow('Stop meas. (min):', self.measureStopSpinbox)

        self.layout.addRow(HorizontalSeparator())

        # Set the button and signals
        self.buttonBox = qtw.QDialogButtonBox( qtw.QDialogButtonBox.Save | qtw.QDialogButtonBox.Cancel )
        self.buttonBox.accepted.connect(self.getSettings)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)

        # Set the layout
        self.setLayout(self.layout)

    # -------------------------------------
    # Get the settings from the controllers
    def getSettings(self):

        # Get the settings from the display
        self.settings = {
        'low_flow': self.lowFlowSpinbox.value(),
        'low_time': self.lowTimeSpinbox.value(),
        'high_flow': self.highFlowSpinbox.value(),
        'high_time': self.highTimeSpinbox.value(),
        'range': [self.measureStartSpinbox.value(), self.measureStopSpinbox.value()],
        }

        # Close the window
        self.accept()
