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
from user_interface._custom_widgets.buttons import ConnectionButton
from user_interface._custom_widgets.comboboxes import AdvComboBox

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setSyringePumpProperties(object):

    def createSyringePumpDisplay(self, parentWidget, add_axis=True):

        # Generate the widget
        self.syringePropertiesWidget = qtw.QWidget()
        self.syringePropertiesLayout = qtw.QGridLayout(self.syringePropertiesWidget)

        ## AXIS AND TYPE ===========================

        crt_row = 0

        if add_axis:

            # Text
            axisLabel = BoldLabel("Axis Port:")
            self.syringePropertiesLayout.addWidget(axisLabel, crt_row, 0)

            # Add the combo box
            self.syringeAxisComboBox = AdvComboBox()
            self.syringeAxisComboBox.addItems( ['X', 'Y', 'Z'] )
            self.syringeAxisComboBox.setToolTip("Axis of the selected pump.")
            self.syringeAxisComboBox.setStatusTip("Axis of the selected pump.")
            self.syringePropertiesLayout.addWidget(self.syringeAxisComboBox, crt_row, 1)

        # Add the type selection
        typeLabel = BoldLabel("Type:")
        self.syringePropertiesLayout.addWidget(typeLabel, crt_row, 2)

        # Add the combo box
        self.syringeTypeComboBox = AdvComboBox()
        self.syringeTypeComboBox.setToolTip("Syringe used on the pump")
        self.syringeTypeComboBox.setStatusTip("Syringe used on the pump")
        self.syringePropertiesLayout.addWidget(self.syringeTypeComboBox, crt_row, 3)

        ## INJECTION SPEED ===========================

        crt_row += 1

        speedLabel = BoldLabel("Flow rate:")
        self.syringePropertiesLayout.addWidget(speedLabel, crt_row, 0)

        # Add the spin box
        self.speedSpinBox = qtw.QDoubleSpinBox()
        self.speedSpinBox.setDecimals(4)
        self.speedSpinBox.setMaximum(10000)
        self.speedSpinBox.setToolTip("Flow rate of the pump")
        self.speedSpinBox.setStatusTip("Flow rate of the pump")
        self.syringePropertiesLayout.addWidget(self.speedSpinBox, crt_row, 1)

        unitLabel = BoldLabel("Unit:")
        self.syringePropertiesLayout.addWidget(unitLabel, crt_row, 2)

        # Add the combo box
        self.speedUnitComboBox = AdvComboBox()
        self.speedUnitComboBox.addItems( ['µL/min', 'mL/s', 'mL/hr', 'µL/hr'] )
        self.speedUnitComboBox.setToolTip( "Unit of the flow rate" )
        self.speedUnitComboBox.setStatusTip( "Unit of the flow rate" )
        self.syringePropertiesLayout.addWidget(self.speedUnitComboBox, crt_row, 3)

        ## OTHER PARAMETERS ===========================

        crt_row += 1

        accelerationLabel = BoldLabel("Acceleration:")
        #self.syringePropertiesLayout.addWidget(accelerationLabel, crt_row, 0)

        # Add the spin box
        self.accelerationSpinBox = qtw.QDoubleSpinBox()
        self.accelerationSpinBox.setMaximum(99999)
        self.accelerationSpinBox.setToolTip("Acceleration of the pump")
        self.accelerationSpinBox.setStatusTip("Acceleration of the pump")
        #self.syringePropertiesLayout.addWidget(self.accelerationSpinBox, crt_row, 1) # Disabled

        self.syringePropertiesLayout.addWidget(qtw.QLabel(''), crt_row, 0, 1, 2) # White space

        gearboxLabel = BoldLabel("Gearbox:")
        self.syringePropertiesLayout.addWidget(gearboxLabel, crt_row, 2)

        # Add the combo box
        self.gearboxComboBox = AdvComboBox()
        self.gearboxComboBox.setToolTip("Gearbox installed on the pump")
        self.gearboxComboBox.setStatusTip("Gearbox installed on the pump")
        self.syringePropertiesLayout.addWidget(self.gearboxComboBox, crt_row,3 )

        # Display the widget
        self.syringePropertiesWidget.setLayout(self.syringePropertiesLayout)
        parentWidget.addWidget(self.syringePropertiesWidget)
