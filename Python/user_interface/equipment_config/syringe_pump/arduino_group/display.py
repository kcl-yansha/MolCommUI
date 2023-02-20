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
from user_interface._custom_widgets.buttons import NeutralButton, AcceptButton, CancelButton
from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.separators import HorizontalSeparator, VerticalSeparator

from user_interface.equipment_config.syringe_pump.arduino_group.functions import setArduinoGroupFunctions
from user_interface.equipment_config.syringe_pump.printed_pump.syringe_properties import setSyringePumpProperties

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setArduinoGroupWindow(qtw.QMainWindow, setArduinoGroupFunctions, setSyringePumpProperties):
    def __init__(self, parent, arduino_class=None):
        super(setArduinoGroupWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setStatusBar(qtw.QStatusBar())

        # Initialise the parameters
        self.active_ports = None
        self.arduino_group = arduino_class
        self.connected = arduino_class is not None
        self.to_load = False

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Set Syringe Group")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createArduinoConnectionDisplay(self.mainLayout)
        self.mainLayout.addWidget(HorizontalSeparator())
        self.createSyringeNavigationDisplay(self.mainLayout)
        self.createSyringePropertiesDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(550, 400))

        # Initialise the appearance of the button
        self.updateConnectButton()
        self.refreshSyringeTypeList()
        self.refreshGearboxList()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the port if open
        if self.connected and not self.to_load:
            print('Cancelling connection to '+self.arduino_group.serial_port+'...')
            print('--------------------')

            self.arduino_group.close()

        # Close the window
        event.accept()
        self.parent.subWindows['arduino_group'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Generate the display to browse the file
    def createArduinoConnectionDisplay(self, parentWidget):

        # Generate the widget
        self.selectionWidget = qtw.QWidget()
        self.selectionLayout = qtw.QGridLayout(self.selectionWidget)

        crt_row = 0

        # Text
        boxLabel = BoldLabel("USB Port:")
        self.selectionLayout.addWidget(boxLabel, crt_row, 0, 1, 4)

        # Refresh button
        self.refreshButton = IconButton(icon_size=25, icon='refresh_button.png')
        self.refreshButton.released.connect(self.refreshPortList)
        self.refreshButton.setToolTip("Refresh the list of active ports.")
        self.refreshButton.setStatusTip("Refresh the list of active ports.")
        self.selectionLayout.addWidget(self.refreshButton, crt_row, 3, 2, 1, alignment=qtc.Qt.AlignBottom)

        crt_row += 1

        # Dropdown for equipment type
        self.portComboBox = qtw.QComboBox()
        self.portComboBox.setToolTip("USB port to connect to.")
        self.portComboBox.setStatusTip("USB port to connect to.")
        self.selectionLayout.addWidget(self.portComboBox, crt_row, 0, 1, 3)

        # Populate the list
        self.refreshPortList()

        crt_row += 1

        # Connect button
        self.connectButton = NeutralButton("Connect")
        self.connectButton.clicked.connect(self.connectGroup)
        self.connectButton.setFixedWidth(150)
        self.connectButton.setToolTip('Connect/Disconnect from the selected port')
        self.connectButton.setStatusTip('Connect/Disconnect from the selected port')
        self.selectionLayout.addWidget(self.connectButton, crt_row, 0)

        nameLabel = BoldLabel("Name:")
        self.selectionLayout.addWidget(nameLabel, crt_row, 1, alignment=qtc.Qt.AlignLeft)

        # Add entry for the syringe name
        self.syringeGroupName = qtw.QLineEdit()
        self.syringeGroupName.setToolTip("Name of the syringe group.")
        self.syringeGroupName.setStatusTip("Name of the syringe group.")
        self.selectionLayout.addWidget(self.syringeGroupName, crt_row, 2)

        # Display the widget
        self.selectionWidget.setLayout(self.selectionLayout)
        parentWidget.addWidget(self.selectionWidget)

    # -------------------------------
    # Generate the navigation display
    def createSyringeNavigationDisplay(self, parentWidget):

        # Generate the widget
        self.navigationWidget = qtw.QWidget()
        self.navigationLayout = qtw.QHBoxLayout(self.navigationWidget)

        # Previous button
        self.previousSyringeButton = IconButton(icon_size=40, icon='previous_button.png')
        self.previousSyringeButton.released.connect(lambda: self.getNextSyringe(increment=-1))
        self.previousSyringeButton.setToolTip("Display the properties of the previous syringe.")
        self.previousSyringeButton.setStatusTip("Display the properties of the previous syringe.")
        self.navigationLayout.addWidget(self.previousSyringeButton)

        # Next button
        self.nextSyringeButton = IconButton(icon_size=40, icon='next_button.png')
        self.nextSyringeButton.released.connect(self.getNextSyringe)
        self.nextSyringeButton.setToolTip("Display the properties of the next syringe.")
        self.nextSyringeButton.setStatusTip("Display the properties of the next syringe.")
        self.navigationLayout.addWidget(self.nextSyringeButton)

        nameLabel = BoldLabel("Syringe Name:")
        self.navigationLayout.addWidget(nameLabel, alignment=qtc.Qt.AlignLeft)

        # Add entry for the syringe name
        self.syringePumpName = qtw.QLineEdit()
        self.syringePumpName.setToolTip("Name of the selected pump.")
        self.syringePumpName.setStatusTip("Name of the selected pump.")
        self.navigationLayout.addWidget(self.syringePumpName)

        # Save button
        self.saveSettingsButton = IconButton(icon_size=40, icon='save_button.png')
        self.saveSettingsButton.released.connect(self.getSaveSettingsMenu)
        self.saveSettingsButton.setToolTip("Save settings.")
        self.saveSettingsButton.setStatusTip("Save settings.")
        self.navigationLayout.addWidget(self.saveSettingsButton)

        # Load button
        self.loadSettingsButton = IconButton(icon_size=40, icon='open_button.png')
        self.loadSettingsButton.released.connect(self.getLoadSettingsMenu)
        self.loadSettingsButton.setToolTip("Load settings.")
        self.loadSettingsButton.setStatusTip("Load settings.")
        self.navigationLayout.addWidget(self.loadSettingsButton)

        self.navigationLayout.addWidget(VerticalSeparator())

        # New button
        self.newSyringeButton = IconButton(icon_size=40, icon='new_button.png')
        self.newSyringeButton.released.connect(self.addNewSyringe)
        self.newSyringeButton.setToolTip("Add a new syringe to the group.")
        self.newSyringeButton.setStatusTip("Add a new syringe to the group.")
        self.navigationLayout.addWidget(self.newSyringeButton)

        # Delete button
        self.deleteSyringeButton = IconButton(icon_size=40, icon='close_button.png')
        self.deleteSyringeButton.released.connect(self.deleteCurrentSyringe)
        self.deleteSyringeButton.setToolTip("Remove the current syringe from the group.")
        self.deleteSyringeButton.setStatusTip("Remove the current syringe from the group.")
        self.navigationLayout.addWidget(self.deleteSyringeButton)

        # Display the widget
        self.navigationWidget.setLayout(self.navigationLayout)
        parentWidget.addWidget(self.navigationWidget)

    # -------------------------------
    # Generate the properties display
    def createSyringePropertiesDisplay(self, parentWidget):

        # Generate the widget
        self.propertiesWidget = qtw.QGroupBox("Properties")
        self.propertiesLayout = qtw.QVBoxLayout(self.propertiesWidget)

        # Add the properties of the syringe
        self.createSyringePumpDisplay(self.propertiesLayout, add_axis=True)

        # Display the widget
        self.propertiesWidget.setLayout(self.propertiesLayout)
        parentWidget.addWidget(self.propertiesWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.setButton = AcceptButton("Set")
        self.setButton.clicked.connect(self.saveSyringeGroup)
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
