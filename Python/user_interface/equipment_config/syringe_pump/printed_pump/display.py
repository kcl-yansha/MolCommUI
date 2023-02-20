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

from user_interface.equipment_config.syringe_pump.printed_pump.functions import setArduinoSyringeFunctions
from user_interface.equipment_config.syringe_pump.printed_pump.syringe_properties import setSyringePumpProperties

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setArduinoSyringeWindow(qtw.QMainWindow,setArduinoSyringeFunctions, setSyringePumpProperties):
    def __init__(self, parent, syringe_class=None, syringe_display=None, display_type='syringe_group'):
        super(setArduinoSyringeWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setStatusBar(qtw.QStatusBar())
        self.syringe_display = syringe_display
        self.display_type = display_type

        # Initialise the parameters
        self.active_ports = None
        self.arduino_syringe = syringe_class
        self.connected = syringe_class is not None

        # Create a timer for button holding
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(lambda: self.movebutton_event_check())
        self.timer_timeout = 500
        self.move_direction = 1

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Syringe Control")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createSyringeNavigationDisplay(self.mainLayout)
        self.createSyringeControlDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(qtc.QSize(550, 300))

        # Initialise the appearance of the button
        self.refreshSyringeTypeList()
        self.refreshGearboxList()
        self.updateProperties()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['syringe_group'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------
    # Generate the navigation display
    def createSyringeNavigationDisplay(self, parentWidget):

        # Generate the widget
        self.navigationWidget = qtw.QWidget()
        self.navigationLayout = qtw.QGridLayout(self.navigationWidget)

        currentRow = 0

        self.navigationLayout.addWidget( BoldLabel("Syringe Name:"), currentRow, 0, alignment=qtc.Qt.AlignLeft )

        # Add entry for the syringe name
        self.syringePumpName = qtw.QLineEdit()
        self.syringePumpName.setToolTip("Name of the selected pump.")
        self.syringePumpName.setStatusTip("Name of the selected pump.")
        self.navigationLayout.addWidget(self.syringePumpName, currentRow, 1)

        # Save button
        self.saveSettingsButton = IconButton(icon_size=40, icon='save_button.png')
        self.saveSettingsButton.released.connect(self.getSaveSettingsMenu)
        self.saveSettingsButton.setToolTip("Save settings.")
        self.saveSettingsButton.setStatusTip("Save settings.")
        self.navigationLayout.addWidget(self.saveSettingsButton, currentRow, 2, 2, 1)

        # Load button
        self.loadSettingsButton = IconButton(icon_size=40, icon='open_button.png')
        self.loadSettingsButton.released.connect(self.getLoadSettingsMenu)
        self.loadSettingsButton.setToolTip("Load settings.")
        self.loadSettingsButton.setStatusTip("Load settings.")
        self.navigationLayout.addWidget(self.loadSettingsButton, currentRow, 3, 2, 1)

        currentRow += 1

        self.navigationLayout.addWidget( BoldLabel("Board:"), currentRow, 0, alignment=qtc.Qt.AlignLeft )

        self.boardLabel = qtw.QLabel( "" )
        self.navigationLayout.addWidget( self.boardLabel, currentRow, 1 )

        # Display the widget
        self.navigationWidget.setLayout(self.navigationLayout)
        parentWidget.addWidget(self.navigationWidget)

    # ---------------------------------------------
    # Make the widget and layout to contain the tab
    def initTab(self):

        # Initialise
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout(widget)

        # Display
        widget.setLayout(layout)

        return widget, layout

    # ----------------------------
    # Generate the control display
    def createSyringeControlDisplay(self, parentWidget):

        # Generate the widget
        self.syringeTabWidget = qtw.QTabWidget()

        # Add the first tab - Properties
        self.propertiesWidget, self.propertiesLayout = self.initTab()
        self.createSyringePumpDisplay(self.propertiesLayout, add_axis=False)
        self.syringeTabWidget.addTab(self.propertiesWidget, 'Properties')

        # Display the widget
        parentWidget.addWidget(self.syringeTabWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.setButton = AcceptButton("Set")
        self.setButton.clicked.connect(self.applySettings)
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
