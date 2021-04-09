import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.buttons import ConnectionButton
from user_interface._custom_widgets.comboboxes import AdvComboBox

from equipment.syringe_pump.properties import getSyringeType

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setSyringePumpProperties(object):

    def createSyringePumpDisplay(self, parentWidget, add_name=True):

        # Generate the widget
        self.syringePropertiesWidget = qtw.QWidget()
        self.syringePropertiesLayout = qtw.QGridLayout(self.syringePropertiesWidget)

        ## NAME ===========================

        crt_row = 0

        if add_name:

            # Text
            nameLabel = BoldLabel("Name:")
            self.syringePropertiesLayout.addWidget(nameLabel, crt_row, 0)

            # Entry line
            self.syringeNameEntry = qtw.QLineEdit('')
            self.syringePropertiesLayout.addWidget(self.syringeNameEntry, crt_row, 1, 1, 3)

            crt_row += 1

        ## AXIS AND TYPE ===========================

        # Text
        axisLabel = BoldLabel("Axis Port:")
        self.syringePropertiesLayout.addWidget(axisLabel, crt_row, 0)

        # Add the combo box
        self.syringeAxisComboBox = AdvComboBox()
        self.syringeAxisComboBox.addItems( ['X', 'Y', 'Z'] )
        self.syringePropertiesLayout.addWidget(self.syringeAxisComboBox, crt_row, 1)

        # Add the type selection
        typeLabel = BoldLabel("Type:")
        self.syringePropertiesLayout.addWidget(typeLabel, crt_row, 2)

        # Add the combo box
        self.syringeTypeComboBox = AdvComboBox()
        self.syringeTypeComboBox.addItems( getSyringeType(return_list = True) )
        self.syringePropertiesLayout.addWidget(self.syringeTypeComboBox, crt_row, 3)

        ## INJECTION SPEED ===========================

        crt_row += 1

        speedLabel = BoldLabel("Speed:")
        self.syringePropertiesLayout.addWidget(speedLabel, crt_row, 0)

        # Add the spin box
        self.speedSpinBox = qtw.QDoubleSpinBox()
        self.speedSpinBox.setDecimals(4)
        self.syringePropertiesLayout.addWidget(self.speedSpinBox, crt_row, 1)

        unitLabel = BoldLabel("Unit:")
        self.syringePropertiesLayout.addWidget(unitLabel, crt_row, 2)

        # Add the combo box
        self.speedUnitComboBox = AdvComboBox()
        self.speedUnitComboBox.addItems( ['mm/s', 'mL/s', 'mL/hr', 'µL/hr'] )
        #self.speedUnitComboBox.addItems( getSyringeType(return_list = True) )
        self.syringePropertiesLayout.addWidget(self.speedUnitComboBox, crt_row, 3)

        ## OTHER PARAMETERS ===========================

        crt_row += 1

        accelerationLabel = BoldLabel("Acceleration:")
        self.syringePropertiesLayout.addWidget(accelerationLabel, crt_row, 0)

        # Add the spin box
        self.accelerationSpinBox = qtw.QDoubleSpinBox()
        self.syringePropertiesLayout.addWidget(self.accelerationSpinBox, crt_row, 1)

        jogLabel = BoldLabel("Jog Delta:")
        self.syringePropertiesLayout.addWidget(jogLabel, crt_row, 2)

        # Add the combo box
        self.jogDeltaComboBox = AdvComboBox()
        self.jogDeltaComboBox.addItems( ['0.01', '0.1', '1.0', '10.0'] )
        #self.speedUnitComboBox.addItems( getSyringeType(return_list = True) )
        self.syringePropertiesLayout.addWidget(self.jogDeltaComboBox, crt_row,3 )

        # Display the widget
        self.syringePropertiesWidget.setLayout(self.syringePropertiesLayout)
        parentWidget.addWidget(self.syringePropertiesWidget)
