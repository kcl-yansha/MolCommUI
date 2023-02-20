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

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.path_to_assets import getIcon

from user_interface.main_window.toolbar.functions import toolBarFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## TOOLBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/

class toolBar (toolBarFunctions):
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent

        # Populate the toolbar
        self.createConnectionToolbar()
        self.createExperimentToolbar()
        self.createSchedulerToolbar()

    # --------------------
    # Populate the toolbar
    def createConnectionToolbar(self):

        # Make the toolbar
        self.connectionToolBar = self.parent.addToolBar("Connection")
        self.connectionToolBar.setMovable(True)

        # Add the button to connect
        self.connectTool = qtw.QAction( getIcon('connect_button.png'), 'Connect to...', self.parent)
        self.connectTool.triggered.connect(self.callEquipmentConnectionWindow)
        self.connectTool.setToolTip("Connect to a new equipment.")
        self.connectTool.setStatusTip("Connect to a new equipment.")
        self.connectionToolBar.addAction( self.connectTool )

    # --------------------
    # Populate the toolbar
    def createExperimentToolbar(self):

        # Make the toolbar
        self.experimentToolBar = self.parent.addToolBar("Experiment")
        self.experimentToolBar.setMovable(True)

        # Add the button to start new experiment
        self.newExperimentTool = qtw.QAction( getIcon('experiment_button.png'), 'New Experiment...', self.parent)
        self.newExperimentTool.triggered.connect(self.callNewExperimentWindow)
        self.newExperimentTool.setToolTip("Start a new experiment.")
        self.newExperimentTool.setStatusTip("Start a new experiment.")
        self.experimentToolBar.addAction( self.newExperimentTool )

        # Add the button to copy the experiment
        self.copyExperiment = qtw.QAction( getIcon('copy_button.png'), 'Copy Experiment...', self.parent)
        self.copyExperiment.triggered.connect(self.copyCurrentExperiment)
        self.copyExperiment.setToolTip("Start a copy of the current experiment.")
        self.copyExperiment.setStatusTip("Start a copy of the current experiment.")
        self.experimentToolBar.addAction( self.copyExperiment )

        self.experimentToolBar.addSeparator()

        # Add the button to start recording the experiment
        self.startRecordingTool = qtw.QAction( getIcon('play_button_green.png'), 'Start Experiment', self.parent)
        self.startRecordingTool.triggered.connect(self.startRecordingExperiment)
        self.startRecordingTool.setToolTip("Start recording the experiment.")
        self.startRecordingTool.setStatusTip("Start recording the experiment.")
        self.experimentToolBar.addAction( self.startRecordingTool )

        # Add the button to stop recording the experiment
        self.stopRecordingTool = qtw.QAction( getIcon('stop_button_red.png'), 'Stop Experiment', self.parent)
        self.stopRecordingTool.triggered.connect(self.stopRecordingExperiment)
        self.stopRecordingTool.setToolTip("Stop recording the experiment.")
        self.stopRecordingTool.setStatusTip("Stop recording the experiment.")
        self.experimentToolBar.addAction( self.stopRecordingTool )

    # --------------------
    # Populate the toolbar
    def createSchedulerToolbar(self):

        # Make the toolbar
        self.schedulerToolBar = self.parent.addToolBar("Scheduler")
        self.schedulerToolBar.setMovable(True)

        # Add the button to start new experiment
        self.openSchedulerTool = qtw.QAction( getIcon('timer.png'), 'Open Scheduler...', self.parent)
        self.openSchedulerTool.triggered.connect(self.callSchedulerWindow)
        self.openSchedulerTool.setToolTip("Open the Scheduler.")
        self.openSchedulerTool.setStatusTip("Open the Scheduler.")
        self.schedulerToolBar.addAction( self.openSchedulerTool )
