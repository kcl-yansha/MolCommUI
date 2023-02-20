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

from settings.equipment.syringe_settings import getSyringeList

from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.browse import Browse
from user_interface._custom_widgets.buttons import AcceptButton, CancelButton
from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.popups.save_settings.syringe_group.functions import saveSyringeSettingsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class saveSyringeSettingsWindow(qtw.QMainWindow, saveSyringeSettingsFunctions):
    def __init__(self, parent, syringe_group=None, syringe_axis=None):
        super(saveSyringeSettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.syringe_group = syringe_group
        self.axis = syringe_axis

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Save Settings...")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createSettingsNameDisplay(self.mainLayout)
        self.createGroupSelectionDisplay(self.mainLayout)
        self.mainLayout.addWidget(HorizontalSeparator())
        self.createSavingSelectionDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Update the UI
        self.updateBrowseStatus()

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['save_settings'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Generate the display to name the file
    def createSettingsNameDisplay(self, parentWidget):

        # Generate the widget
        self.nameWidget = qtw.QWidget()
        self.nameLayout = qtw.QHBoxLayout(self.nameWidget)

        # Make the label for the name
        self.nameLayout.addWidget( BoldLabel('Name:') )

        # Field to edit the name
        self.nameEntry = qtw.QLineEdit()
        self.nameEntry.setText('Default')
        self.nameLayout.addWidget( self.nameEntry )

        # Display the widget
        self.nameWidget.setLayout(self.nameLayout)
        parentWidget.addWidget(self.nameWidget)

    # -------------------------------------
    # Generate the display to name the file
    def createGroupSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.groupWidget = qtw.QWidget()
        self.groupLayout = qtw.QHBoxLayout(self.groupWidget)

        self.groupButton = qtw.QRadioButton("Syringe Group settings")
        self.groupLayout.addWidget( self.groupButton )

        self.syringeButton = qtw.QRadioButton("Syringe settings")
        self.syringeButton.setChecked(True)
        self.groupLayout.addWidget( self.syringeButton )

        # Display the widget
        self.groupWidget.setLayout(self.groupLayout)
        parentWidget.addWidget(self.groupWidget)

    # ---------------------------------------
    # Generate the display to browse the file
    def createSavingSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.selectionWidget = qtw.QWidget()
        self.selectionLayout = qtw.QVBoxLayout(self.selectionWidget)

        # Checkbox for save in settings
        self.settingsCheckbox = qtw.QCheckBox("Save in local settings?")
        self.settingsCheckbox.setChecked(True)
        self.selectionLayout.addWidget( self.settingsCheckbox )

        # Checkbox for save in file
        self.fileCheckbox = qtw.QCheckBox("Save in file?")
        self.fileCheckbox.stateChanged.connect(self.updateBrowseStatus)
        self.selectionLayout.addWidget( self.fileCheckbox )

        # Browse for the file image path
        self.fileBrowsing = Browse()
        self.fileBrowsing.connectButton(self.browsePath)
        self.selectionLayout.addWidget( self.fileBrowsing )

        # Display the widget
        self.selectionWidget.setLayout(self.selectionLayout)
        parentWidget.addWidget(self.selectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = AcceptButton("Save")
        self.saveButton.clicked.connect(self.saveSelectionSettings)
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
