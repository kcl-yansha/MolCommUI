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

from user_interface.scheduler.main_scheduler.functions import setSchedulerFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setSchedulerWindow(qtw.QMainWindow, setSchedulerFunctions):
    def __init__(self, parent):
        super(setSchedulerWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.events = self.parent.scheduler_elements.copy()

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Set Scheduler")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createManagerDisplay(self.mainLayout)
        self.createSavingActions(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(600, 325))

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['set_scheduler'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the controls for the user
    def createManagerDisplay(self, parentWidget):

        # Generate the widget
        self.schedulerManagerWidget = qtw.QWidget()
        self.schedulerManagerLayout = qtw.QHBoxLayout(self.schedulerManagerWidget)

        # Populate
        self.createEventTableWidget(self.schedulerManagerLayout)
        self.createEventControllerWidget(self.schedulerManagerLayout)

        # Display the widget
        self.schedulerManagerWidget.setLayout(self.schedulerManagerLayout)
        parentWidget.addWidget(self.schedulerManagerWidget)

    # -----------------------------------------
    # Generate the table display for the events
    def createEventTableWidget(self, parentWidget):

        # Generate the widget
        self.schedulerEventWidget = qtw.QWidget()
        self.schedulerEventLayout = qtw.QVBoxLayout(self.schedulerEventWidget)

        # Generate the table of servers
        self.eventTable = CTableWidget(0, 6)
        self.eventTable.setLabels( ['', '', 'Event', '', '', 'Pumps'] )

        self.eventTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.eventTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        self.eventTable.setShowGrid(False)
        self.eventTable.setMinimumHeight(100)
        self.eventTable.setFixedWidth(350)
        self.schedulerEventLayout.addWidget(self.eventTable)

        # Populate the widget
        self.fillEventTable()

        # Display the widget
        self.schedulerEventWidget.setLayout(self.schedulerEventLayout)
        parentWidget.addWidget(self.schedulerEventWidget)

    # --------------------------------------
    # Generate the controllers for the event
    def createEventControllerWidget(self, parentWidget):

        # Generate the widget
        self.evenControlWidget = qtw.QWidget()
        self.evenControlLayout = qtw.QVBoxLayout(self.evenControlWidget)

        self.evenControlLayout.addWidget(BoldLabel('Pump(s):'))

        # Add a constant flowrate
        self.addConstantButton = qtw.QPushButton("Add Constant")
        self.addConstantButton.clicked.connect(lambda x:self.editConstant(None))
        self.evenControlLayout.addWidget(self.addConstantButton)

        # Add the stop command
        self.addStopButton = qtw.QPushButton("Add Stop")
        self.addStopButton.clicked.connect(lambda x:self.editStop(None))
        self.evenControlLayout.addWidget(self.addStopButton)

        self.evenControlLayout.addWidget(HorizontalSeparator())

        self.evenControlLayout.addWidget(BoldLabel('General:'))

        # Add a wait
        self.addWaitButton = qtw.QPushButton("Add Wait")
        self.addWaitButton.clicked.connect(lambda x:self.editWait(None))
        self.evenControlLayout.addWidget(self.addWaitButton)

        # Add a toggle
        self.addExpToggleButton = qtw.QPushButton("Toggle Experiment")
        self.addExpToggleButton.clicked.connect(lambda x:self.editExperimentToggle(None))
        self.evenControlLayout.addWidget(self.addExpToggleButton)

        # Display the widget
        self.evenControlWidget.setLayout(self.evenControlLayout)
        parentWidget.addWidget(self.evenControlWidget)

    # ----------------------------------------
    # Generate the saving and loading controls
    def createSavingActions(self, parentWidget):

        # Generate the widget
        self.saveActionsWidget = qtw.QWidget()
        self.saveActionsLayout = qtw.QHBoxLayout(self.saveActionsWidget)

        # Save button
        self.saveSettingsButton = IconButton(icon_size=35, icon='save_button.png')
        self.saveSettingsButton.released.connect(self.saveInFile)
        self.saveSettingsButton.setToolTip("Save schedule.")
        self.saveActionsLayout.addWidget(self.saveSettingsButton)

        # Load button
        self.loadSettingsButton = IconButton(icon_size=35, icon='open_button.png')
        self.loadSettingsButton.released.connect(self.loadFromFile)
        self.loadSettingsButton.setToolTip("Load schedule.")
        self.saveActionsLayout.addWidget(self.loadSettingsButton)

        # Display the widget
        self.saveActionsWidget.setLayout(self.saveActionsLayout)
        parentWidget.addWidget(self.saveActionsWidget, alignment=qtc.Qt.AlignLeft)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.newButton = AcceptButton("Set")
        self.newButton.clicked.connect(self.saveScheduler)
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
