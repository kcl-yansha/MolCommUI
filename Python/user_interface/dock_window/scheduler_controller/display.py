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

import pyqtgraph as pg
import time

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.separators import VerticalSeparator

from user_interface.dock_window.scheduler_controller.functions import SchedulerControllerFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class SchedulerControllerPanel(qtw.QDockWidget, SchedulerControllerFunctions):
    def __init__(self, name, parent):
        super(SchedulerControllerPanel, self).__init__(name, parent)

                # Initialise the subwindow
        self.parent = parent
        self.setAllowedAreas( qtc.Qt.TopDockWidgetArea | qtc.Qt.BottomDockWidgetArea )

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QHBoxLayout(self.mainWidget)

        # Populate the panel
        self.createCommandDisplay(self.mainLayout)
        self.mainLayout.addWidget(VerticalSeparator())
        self.createSequenceDisplay(self.mainLayout)

        # Display the panel
        self.mainLayout.setAlignment(qtc.Qt.AlignTop)
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        #self.show()
        #self.setMinimumSize(550,650)

        self.updateStatus(self.parent.scheduler_running)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()

        # Disconnect the dock from the software
        self.parent.removeDockWidget(self.parent.docks["scheduler"])
        self.parent.docks["scheduler"] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------
    # Generate the widget with the user actions
    def createCommandDisplay(self, parentWidget):

        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QHBoxLayout(self.buttonWidget)

        # Baseline
        self.toggleRunButton = qtw.QPushButton('Toggle Scheduler')
        self.toggleRunButton.setFixedHeight(40)
        self.toggleRunButton.released.connect(self.toggleScheduler)
        self.buttonLayout.addWidget(self.toggleRunButton)

        self.statusWidget = qtw.QWidget()
        self.statusLayout = qtw.QVBoxLayout(self.statusWidget)

        # Display
        self.schedulerStatusOn = qtw.QLabel('Scheduler is on')
        self.statusLayout.addWidget(self.schedulerStatusOn)

        self.schedulerStatusOff = qtw.QLabel('Scheduler is off')
        self.statusLayout.addWidget(self.schedulerStatusOff)

        self.statusWidget.setLayout(self.statusLayout)
        self.buttonLayout.addWidget(self.statusWidget)

        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)

    # -----------------------------------------
    # Generate the widget with the user actions
    def createSequenceDisplay(self, parentWidget):

        self.sequenceWidget = qtw.QWidget()
        self.sequenceLayout = qtw.QVBoxLayout(self.sequenceWidget)

        # Display
        self.schedulerNote = BoldLabel('Current: None')
        self.sequenceLayout.addWidget(self.schedulerNote)

        self.schedulerPastNote = qtw.QLabel('Next: None')
        self.sequenceLayout.addWidget(self.schedulerPastNote)

        self.sequenceWidget.setLayout(self.sequenceLayout)
        parentWidget.addWidget(self.sequenceWidget)
