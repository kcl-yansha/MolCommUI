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

from multithreading.scheduler import Scheduler

from settings.user import loadMainConfig, getUserConfig, editUserConfigValue

from user_interface._style.color_theme import applyStyle
from input_output.experiments.experiment_class import setExperiment

from user_interface.main_window.manage_experiments import mainGUIExperimentFunctions
from user_interface.main_window.preload_equipment import mainGUIPreloadFunctions
from user_interface.main_window.menubar.display import menuBar
from user_interface.main_window.toolbar.display import toolBar

from user_interface.experiments.main_widget.display import experimentDisplay

from user_interface.groups.group_interface.display import EquipmentGroups

##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUI(qtw.QMainWindow, mainGUIPreloadFunctions, mainGUIExperimentFunctions, Scheduler):
    def __init__(self, application):
        super(mainGUI, self).__init__()

        # Initialize the properties of the software Main GUI
        self.application = application
        self.title = "MolCommUI"
        self.version = "v1.0"

        # Load the user profile
        self.main_config = loadMainConfig()
        self.loadUser()
        self.current_folder = self.user_config['save_folder']

        # Initialise an experiment
        self.experiment = setExperiment(self)

        # Initialize the sub-windows and docks containers
        self.subWindows = {}
        self.docks = {
        'scheduler': None,
        'graph': None,
        'spectrum': None,
        'terminal': None
        }

        # Initialise the list of threads
        print("Multithreading with maximum %d threads" % qtc.QThreadPool().maxThreadCount())
        self.threads = {}

        # Initialize the list of equipment
        self.active_ports = []
        self.equipments = {
        'syringe_pumps':[],
        'peristaltic_pumps':[],
        'flow_meter':[],
        'valve_group':[],
        'spectrometer':[]
        }

        # Generate the display
        self.setWindowTitle(self.title + " (" + self.version + ")")

        # Apply the style
        applyStyle( self.application )

        # Generate the central widget
        self.createCentralWidget()

        # Add the status bar to the window
        self.statusBar = qtw.QStatusBar()
        self.setStatusBar(self.statusBar)

        # Add the menu and toolbars
        self.menuBar = menuBar(self)
        self.toolBar = toolBar(self)

        # Display the window
        self.show()
        self.setMinimumSize(575,725)

        # Load the equipment if any
        self.preloadEquipment()
        self.experimentDisplay.setExperimentName(self.experiment.name)
        self.experimentDisplay.setExperimentStatus(self.experiment.recording)

        # Initialise the scheduler
        self.resetScheduler()

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## DISPLAY THE MAIN WINDOW
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Create the central widget of the window
    def createCentralWidget(self):

        # Define the widget
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Get the experiment display
        self.experimentDisplay = experimentDisplay(self)
        self.mainLayout.addWidget(self.experimentDisplay)

        # Display the group display
        self.groupDisplay = EquipmentGroups(self)
        self.mainLayout.addWidget(self.groupDisplay)

        # Display the widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # -----------------------------
    # Get the list of all equipment
    def listEquipment(self):

        # Initialise the list
        equipment_list = {}

        # Check the syringe pumps
        for syringe in self.equipments['syringe_pumps']:
            if syringe.syringe_group.serial_port not in equipment_list.keys():
                equipment_list[syringe.syringe_group.serial_port] = ['Syringe group', syringe.syringe_group]

        # Check the flowmeters
        for flowmeter in self.equipments['flow_meter']:
            equipment_list[flowmeter.serial_port] = ['Flowmeter', flowmeter]

        return equipment_list

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## CHANGE THE SOFTWARE CONFIG
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Load the selected user profile
    def loadUser(self):

        # Get the new user to load
        user_to_load = self.main_config['current_user']

        # Save the new user in the config file
        self.editConfig('current_user', user_to_load, from_user=False)

        # Load the config for the user
        self.user_config = getUserConfig( user_to_load )

        # Print a message
        print('Configuration for ' + user_to_load + ' loaded in the software...')
        print('--------------------')

    # ----------------------------
    # Edit the value in the config
    def editConfig(self, key, value, from_user=True):

        # Modify the user settings
        if from_user:
            self.user_config[key] = value
            editUserConfigValue(self.main_config['current_user'], key, value)

        # Modify the main settings
        else:
            self.main_config[key] = value
            editUserConfigValue('MAIN', key, value)
