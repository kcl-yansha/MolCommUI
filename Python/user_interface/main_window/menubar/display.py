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

from user_interface.main_window.menubar.functions_files import menuBarFilesFunctions
from user_interface.main_window.menubar.functions_equipment import menuBarEquipmentFunctions
from user_interface.main_window.menubar.functions_window import menuBarWindowFunctions
from user_interface.main_window.menubar.functions_help import menuBarHelpFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## MENUBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/

class menuBar (menuBarFilesFunctions, menuBarEquipmentFunctions, menuBarWindowFunctions, menuBarHelpFunctions):
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent
        self.mainMenu = self.parent.menuBar()
        self.mainMenu.setNativeMenuBar(False)

        # Call the different submenus
        self.createFileMenu()
        self.createEquipmentMenu()
        self.createWindowMenu()
        self.createHelpMenu()

    ##-\-\-\-\-\-\-\-\-\-\
    ## INTERFACE GENERATION
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------
    # Generate the FILE submenu
    def createFileMenu(self):

        # Initialise
        self.fileMenu = self.mainMenu.addMenu("File")
        self.fileMenu.setToolTipsVisible(True)

        # Start new experiment
        self.fileMenu.newExperiment = qtw.QAction("New Experiment", self.parent)
        self.fileMenu.newExperiment.setToolTip("Start a new experiment.")
        self.fileMenu.newExperiment.setStatusTip("Start a new experiment.")
        self.fileMenu.newExperiment.triggered.connect(self.callNewExperiment)
        self.fileMenu.newExperiment.setShortcut("Ctrl+N")
        self.fileMenu.addAction(self.fileMenu.newExperiment)

        self.fileMenu.addSeparator()

        # Exit the software
        self.fileMenu.quitButton = qtw.QAction("Quit", self.parent)
        self.fileMenu.quitButton.setShortcut("Ctrl+Q")
        self.fileMenu.quitButton.setToolTip("Close the software.")
        self.fileMenu.quitButton.setStatusTip("Close the software.")
        self.fileMenu.quitButton.triggered.connect(self.parent.close)
        self.fileMenu.addAction(self.fileMenu.quitButton)

    # ------------------------------
    # Generate the EQUIPMENT submenu
    def createEquipmentMenu(self):

        # Initialise
        self.equipmentMenu = self.mainMenu.addMenu("Equipment")
        self.equipmentMenu.setToolTipsVisible(True)

        # Connect to equipment
        self.equipmentMenu.connectToSubmenu = qtw.QMenu('Connect to...', self.parent)
        self.equipmentMenu.connectToSubmenu.setToolTipsVisible(True)

        # Add Syringe pump
        self.equipmentMenu.syringePump = qtw.QAction("Syringe Pump", self.parent)
        self.equipmentMenu.syringePump.setToolTip("Connect to a syringe pump.")
        self.equipmentMenu.syringePump.setStatusTip("Connect to a syringe pump.")
        self.equipmentMenu.syringePump.triggered.connect(self.callSyringeGroupWindow)
        self.equipmentMenu.connectToSubmenu.addAction(self.equipmentMenu.syringePump)

        # Add Flow meter
        self.equipmentMenu.flowMeter = qtw.QAction("Flow Meter", self.parent)
        self.equipmentMenu.flowMeter.setToolTip("Connect to a flow meter.")
        self.equipmentMenu.flowMeter.setStatusTip("Connect to a flow meter.")
        self.equipmentMenu.flowMeter.triggered.connect(self.callFlowMeterWindow)
        self.equipmentMenu.connectToSubmenu.addAction(self.equipmentMenu.flowMeter)

        # Add Spectrometer
        self.equipmentMenu.spectroMeter = qtw.QAction("Spectrometer", self.parent)
        self.equipmentMenu.spectroMeter.setToolTip("Connect to a spectrometer.")
        self.equipmentMenu.spectroMeter.setStatusTip("Connect to a spectrometer.")
        self.equipmentMenu.spectroMeter.triggered.connect(self.callSpectrometerWindow)
        self.equipmentMenu.connectToSubmenu.addAction(self.equipmentMenu.spectroMeter)

        self.equipmentMenu.addMenu(self.equipmentMenu.connectToSubmenu)

        # Manage experiments
        self.equipmentMenu.manageEquipment = qtw.QAction("Manage Equipments", self.parent)
        self.equipmentMenu.manageEquipment.setToolTip("Manage the opened equipments.")
        self.equipmentMenu.manageEquipment.setStatusTip("Manage the opened equipments.")
        self.equipmentMenu.manageEquipment.triggered.connect(self.callEquipmentManagement)
        self.equipmentMenu.addAction(self.equipmentMenu.manageEquipment)

        self.equipmentMenu.addSeparator()

        # Connect to equipment
        self.equipmentMenu.calibrateSubmenu = qtw.QMenu('Calibrate...', self.parent)
        self.equipmentMenu.calibrateSubmenu.setToolTipsVisible(True)

        # Add PID controller calibration
        self.equipmentMenu.calPID = qtw.QAction("PID Controllers", self.parent)
        self.equipmentMenu.calPID.setToolTip("Calibrate the PID controllers.")
        self.equipmentMenu.calPID.setStatusTip("Calibrate the PID controllers.")
        self.equipmentMenu.calPID.triggered.connect(self.callPIDControllerCalibrateWindow)
        self.equipmentMenu.calibrateSubmenu.addAction(self.equipmentMenu.calPID)

        self.equipmentMenu.calibrateSubmenu.addSeparator()

        # Add Syringe calibration
        self.equipmentMenu.calSyringePump = qtw.QAction("Syringes", self.parent)
        self.equipmentMenu.calSyringePump.setToolTip("Calibrate the syringes.")
        self.equipmentMenu.calSyringePump.setStatusTip("Calibrate the syringes.")
        self.equipmentMenu.calSyringePump.triggered.connect(self.callSyringeCalibrateWindow)
        self.equipmentMenu.calibrateSubmenu.addAction(self.equipmentMenu.calSyringePump)

        # Add Gearbox calibration
        self.equipmentMenu.calGearBox = qtw.QAction("Gearboxes", self.parent)
        self.equipmentMenu.calGearBox.setToolTip("Calibrate the gearboxes.")
        self.equipmentMenu.calGearBox.setStatusTip("Calibrate the gearboxes.")
        self.equipmentMenu.calGearBox.triggered.connect(self.callGearboxCalibrateWindow)
        self.equipmentMenu.calibrateSubmenu.addAction(self.equipmentMenu.calGearBox)

        self.equipmentMenu.calibrateSubmenu.addSeparator()

        # Add Flowmeter calibration
        self.equipmentMenu.calFlowmeter = qtw.QAction("Flowmeters", self.parent)
        self.equipmentMenu.calFlowmeter.setToolTip("Calibrate the flowmeters.")
        self.equipmentMenu.calFlowmeter.setStatusTip("Calibrate the flowmeters.")
        self.equipmentMenu.calFlowmeter.triggered.connect(self.callFlowmeterCalibrateWindow)
        self.equipmentMenu.calibrateSubmenu.addAction(self.equipmentMenu.calFlowmeter)

        self.equipmentMenu.addMenu(self.equipmentMenu.calibrateSubmenu)

    # ---------------------------
    # Generate the WINDOW submenu
    def createWindowMenu(self):

        # Initialise
        self.windowMenu = self.mainMenu.addMenu("Window")
        self.windowMenu.setToolTipsVisible(True)

        # Open scheduler
        self.windowMenu.schedulerControllerButton = qtw.QAction("Scheduler", self.parent)
        self.windowMenu.schedulerControllerButton.setShortcut("Ctrl+Alt+S")
        self.windowMenu.schedulerControllerButton.setToolTip("Display the scheduler dock.")
        self.windowMenu.schedulerControllerButton.setStatusTip("Display the scheduler dock.")
        self.windowMenu.schedulerControllerButton.triggered.connect(self.callSchedulerControllerDock)
        self.windowMenu.addAction(self.windowMenu.schedulerControllerButton)

        # Open spectrum window
        self.windowMenu.spectrumDisplayButton = qtw.QAction("Spectrum Display", self.parent)
        self.windowMenu.spectrumDisplayButton.setToolTip("Display the intensity spectrum window.")
        self.windowMenu.spectrumDisplayButton.setStatusTip("Display the intensity spectrum window.")
        self.windowMenu.spectrumDisplayButton.triggered.connect(self.callSpectrumDisplayDock)
        self.windowMenu.addAction(self.windowMenu.spectrumDisplayButton)

    # -------------------------
    # Generate the HELP submenu
    def createHelpMenu(self):

        # Initialise
        self.helpMenu = self.mainMenu.addMenu("Help")
        self.helpMenu.setToolTipsVisible(True)

        # Edit the user settings
        self.helpMenu.userSettingsButton = qtw.QAction("Settings", self.parent)
        self.helpMenu.userSettingsButton.setToolTip("Edit the settings of the software.")
        self.helpMenu.userSettingsButton.setStatusTip("Edit the settings of the software.")
        self.helpMenu.userSettingsButton.triggered.connect(self.callUserSettingsWindow)
        self.helpMenu.addAction(self.helpMenu.userSettingsButton)

        self.helpMenu.addSeparator()

        # Edit the user settings
        self.helpMenu.debugModeButton = qtw.QAction("Debug", self.parent)
        self.helpMenu.debugModeButton.setToolTip("Open the Debug Mode settings.")
        self.helpMenu.debugModeButton.setStatusTip("Open the Debug Mode settings.")
        self.helpMenu.debugModeButton.triggered.connect(self.callDebugSettingsWindow)
        self.helpMenu.addAction(self.helpMenu.debugModeButton)

        self.helpMenu.addSeparator()

        # Edit the user settings
        self.helpMenu.aboutButton = qtw.QAction("About...", self.parent)
        self.helpMenu.aboutButton.setToolTip("General information on the software.")
        self.helpMenu.aboutButton.setStatusTip("General information on the software.")
        self.helpMenu.aboutButton.triggered.connect(self.callAboutWindow)
        self.helpMenu.addAction(self.helpMenu.aboutButton)
