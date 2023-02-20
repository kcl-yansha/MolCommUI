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
from user_interface._custom_widgets.browse import Browse
from user_interface._custom_widgets.buttons import AcceptButton, CancelButton
from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.popups.debug_settings.functions import debugSettingsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class debugSettingsWindow(qtw.QMainWindow, debugSettingsFunctions):
    def __init__(self, parent):
        super(debugSettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Debug Mode")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createTabDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(550, 400))

        # Initialise the appearance of the button
        #self.updateConnectButton()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['debug_settings'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------
    # Make the widget and layout to contain the tab
    def initTab(self):

        # Initialise
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout(widget)

        # Display
        widget.setLayout(layout)

        return widget, layout

    # ---------------------------
    # Generate the name selection
    def createTabDisplay(self, parentWidget):

        # Generate the widget
        self.tabWidget = qtw.QTabWidget()

        # Add the first tab - Syringe Pumps
        self.syringePumpWidget, self.syringePumpLayout = self.initTab()
        self.createSyringePumpSettingsDisplay(self.syringePumpLayout)
        self.tabWidget.addTab(self.syringePumpWidget, 'Syringe Pump(s)')

        # Add the second tab - Flow meters
        self.flowMeterWidget, self.flowMeterLayout = self.initTab()
        self.createFlowMeterSettingsDisplay(self.flowMeterLayout)
        self.tabWidget.addTab(self.flowMeterWidget, 'Flow Meter(s)')

        # Display the widget
        parentWidget.addWidget(self.tabWidget)

    # -------------------------------------------
    # Generate the settings for the syringe pumps
    def createSyringePumpSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.syringeSettingsWidget = qtw.QWidget()
        self.syringeSettingsLayout = qtw.QVBoxLayout(self.syringeSettingsWidget)

        # Add the dated folder option
        self.syringeSendCommandCheckbox = qtw.QCheckBox('Write in file commands sent to pumps?')
        self.syringeSendCommandCheckbox.setChecked( self.parent.main_config['debug_syringe_send'] )
        self.syringeSettingsLayout.addWidget( self.syringeSendCommandCheckbox )

        # Add the dated folder option
        self.syringeVerboseCheckbox = qtw.QCheckBox('Enable verbose mode?')
        self.syringeVerboseCheckbox.setChecked( self.parent.main_config['debug_syringe'] )
        self.syringeSettingsLayout.addWidget( self.syringeVerboseCheckbox )

        # Display the widget
        self.syringeSettingsWidget.setLayout(self.syringeSettingsLayout)
        parentWidget.addWidget(self.syringeSettingsWidget)

    # -------------------------------------------
    # Generate the settings for the syringe pumps
    def createFlowMeterSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.flowmeterSettingsWidget = qtw.QWidget()
        self.flowmeterSettingsLayout = qtw.QVBoxLayout(self.flowmeterSettingsWidget)

        # Add the dated folder option
        self.flowMeterVerboseCheckbox = qtw.QCheckBox('Enable verbose mode?')
        self.flowMeterVerboseCheckbox.setChecked( self.parent.main_config['debug_flowmeter'] )
        self.flowmeterSettingsLayout.addWidget( self.flowMeterVerboseCheckbox )

        # Display the widget
        self.flowmeterSettingsWidget.setLayout(self.flowmeterSettingsLayout)
        parentWidget.addWidget(self.flowmeterSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = AcceptButton("Save")
        self.saveButton.clicked.connect(self.saveDebugSettings)
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
