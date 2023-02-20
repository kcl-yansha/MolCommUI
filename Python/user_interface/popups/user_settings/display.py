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

from user_interface.popups.user_settings.functions import userSettingsFunctions

from settings.equipment.reload_equipment import getEquipmentList

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class userSettingsWindow(qtw.QMainWindow, userSettingsFunctions):
    def __init__(self, parent):
        super(userSettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Settings")
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
        self.parent.subWindows['user_settings'] = None

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

        # Add the first tab - General
        self.generalWidget, self.generalLayout = self.initTab()
        self.createGeneralSettingsDisplay(self.generalLayout)
        self.tabWidget.addTab(self.generalWidget, 'General')

        # Display the widget
        parentWidget.addWidget(self.tabWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createGeneralSettingsDisplay(self, parentWidget):

        # Generate the widget
        self.generalSettingsWidget = qtw.QWidget()
        self.generalSettingsLayout = qtw.QVBoxLayout(self.generalSettingsWidget)

        # Browse for the folder
        self.generalSettingsLayout.addWidget( BoldLabel('Default folder:') )

        self.defaultFolderBrowser = Browse()
        self.defaultFolderBrowser.setText( self.parent.user_config['save_folder'] )
        self.defaultFolderBrowser.connectButton(self.browseDefaultFolder)
        self.generalSettingsLayout.addWidget( self.defaultFolderBrowser )

        # Add the dated folder option
        self.datedFolderCheckbox = qtw.QCheckBox('Automatically generate dated folder')
        self.datedFolderCheckbox.setChecked( self.parent.user_config['use_date'] )
        self.generalSettingsLayout.addWidget( self.datedFolderCheckbox )

        self.generalSettingsLayout.addWidget( HorizontalSeparator() )

        # Add the autoload equipment option
        is_enabled, _ = getEquipmentList( user_name=self.parent.main_config['current_user'] )

        self.loadEquipmentCheckbox = qtw.QCheckBox('Autoload equipment on start?')
        self.loadEquipmentCheckbox.setChecked( is_enabled )
        self.generalSettingsLayout.addWidget( self.loadEquipmentCheckbox )

        # Display the widget
        self.generalSettingsWidget.setLayout(self.generalSettingsLayout)
        parentWidget.addWidget(self.generalSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = AcceptButton("Save")
        self.saveButton.clicked.connect(self.saveUserSettings)
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
