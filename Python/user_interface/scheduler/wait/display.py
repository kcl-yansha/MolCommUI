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
from user_interface._custom_widgets.buttons import AcceptButton, CancelButton
from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.separators import HorizontalSeparator, VerticalSeparator
from user_interface._custom_widgets.table import CTableWidget

from user_interface.scheduler.wait.functions import setWaitFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setWaitWindow(qtw.QMainWindow, setWaitFunctions):
    def __init__(self, parent, event=None, parent_widget=None):
        super(setWaitWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.event = event
        self.parent_widget = parent_widget

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Set Wait")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createWaitSettings(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(425, 300))

        # Initialise the display
        self.initInterface()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['edit_wait'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the controls for the user
    def createWaitSettings(self, parentWidget):

        # Generate the widget
        self.schedulerManagerWidget = qtw.QGroupBox('Settings')
        self.schedulerManagerLayout = qtw.QFormLayout(self.schedulerManagerWidget)

        self.valueDuration = qtw.QDoubleSpinBox()
        self.valueDuration.setValue(2.0)
        self.valueDuration.setDecimals(4)
        self.valueDuration.setMaximum(1000)
        self.schedulerManagerLayout.addRow(qtw.QLabel('Duration (min)'), self.valueDuration)

        # Display the widget
        self.schedulerManagerWidget.setLayout(self.schedulerManagerLayout)
        parentWidget.addWidget(self.schedulerManagerWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.newButton = AcceptButton("Set")
        self.newButton.clicked.connect(self.setWait)
        self.newButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.newButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
