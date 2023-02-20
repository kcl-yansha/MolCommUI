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

from user_interface._custom_widgets.browse import Browse
from user_interface._custom_widgets.buttons import AcceptButton, CancelButton
from user_interface._custom_widgets.comboboxes import AdvComboBox
from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.popups.load_settings.syringe_group.functions import loadSyringeSettingsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class loadSyringeSettingsWindow(qtw.QMainWindow, loadSyringeSettingsFunctions):
    def __init__(self, parent, interface=None, syringe_group=None, syringe_axis=None):
        super(loadSyringeSettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.interface = interface
        self.syringe_group = syringe_group
        self.axis = syringe_axis

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Load Settings...")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createSettingsSourceDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Initialise the UI
        self.updateComboboxSelection()

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['load_settings'] = None

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

    # ----------------------------
    # Generate the control display
    def createSettingsSourceDisplay(self, parentWidget):

        # Generate the widget
        self.syringeTabWidget = qtw.QTabWidget()

        # Add the first tab - Properties
        self.localWidget, self.localLayout = self.initTab()
        self.createGroupSelectionDisplay(self.localLayout)
        self.syringeTabWidget.addTab(self.localWidget, 'Local Settings')

        # Add the first tab - Properties
        self.fileWidget, self.fileLayout = self.initTab()
        self.createSavingSelectionDisplay(self.fileLayout)
        self.syringeTabWidget.addTab(self.fileWidget, 'Settings File')

        # Display the widget
        parentWidget.addWidget(self.syringeTabWidget)

    # -------------------------------------
    # Generate the display to name the file
    def createGroupSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.groupWidget = qtw.QWidget()
        self.groupLayout = qtw.QVBoxLayout(self.groupWidget)

        # Generate the combobox field
        self.radioWidget = qtw.QWidget()
        self.radioLayout = qtw.QHBoxLayout(self.radioWidget)

        # Make the radio button
        self.groupButton = qtw.QRadioButton("Syringe Group settings")
        self.radioLayout.addWidget( self.groupButton )

        self.syringeButton = qtw.QRadioButton("Syringe settings")
        self.syringeButton.setChecked(True)
        self.syringeButton.toggled.connect(self.updateComboboxSelection)
        self.radioLayout.addWidget( self.syringeButton )

        # Display the radiobutton group
        self.radioWidget.setLayout(self.radioLayout)
        self.groupLayout.addWidget(self.radioWidget)

        # Add the combo box
        self.syringeSettingsComboBox = AdvComboBox()
        self.groupLayout.addWidget( self.syringeSettingsComboBox )

        # Display the widget
        self.groupWidget.setLayout(self.groupLayout)
        parentWidget.addWidget(self.groupWidget)

    # ---------------------------------------
    # Generate the display to browse the file
    def createSavingSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.selectionWidget = qtw.QWidget()
        self.selectionLayout = qtw.QVBoxLayout(self.selectionWidget)

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
        self.loadButton = AcceptButton("Load")
        self.loadButton.clicked.connect(self.loadSelection)
        self.loadButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.loadButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
