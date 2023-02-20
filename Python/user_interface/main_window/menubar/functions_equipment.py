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

from user_interface._common_functions.window_handling import openWindow

from user_interface.equipment_config.syringe_pump.arduino_group.display import setArduinoGroupWindow
from user_interface.equipment_config.flow_meter.display import setFlowMeterWindow
from user_interface.equipment_config.spectrometer.connection.display import setSpectroMeterWindow

from user_interface.equipment_config.manager.display import manageEquipmentWindow

from user_interface.equipment_calibration.syringes.manager.display import calibrateSyringeWindow
from user_interface.equipment_calibration.flowmeters.manager.display import calibrateFlowmeterWindow
from user_interface.equipment_calibration.pid_controllers.manager.display import calibratePIDWindow
from user_interface.equipment_calibration.gearboxes.manager.display import calibrateGearboxWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarEquipmentFunctions(object):

    ##-\-\-\-\-\-\
    ## Window MENU
    ##-/-/-/-/-/-/

    # --------------------------
    # Open the connection window
    def callSyringeGroupWindow(self):
        openWindow(self.parent, setArduinoGroupWindow, 'arduino_group')

    # --------------------------
    # Open the connection window
    def callPeristalticGroupWindow(self):
        openWindow(self.parent, setPeristalticGroupWindow, 'peristaltic_group')

    # --------------------------
    # Open the connection window
    def callMicropumpGroupWindow(self):
        openWindow(self.parent, setMicropumpGroupWindow, 'micropump_group')

    # --------------------------
    # Open the connection window
    def callFlowMeterWindow(self):
        openWindow(self.parent, setFlowMeterWindow, 'flow_meter')

    # --------------------------
    # Open the connection window
    def callValveWindow(self):
        openWindow(self.parent, setValveGroupWindow, 'valves')

    # --------------------------
    # Open the connection window
    def callSpectrometerWindow(self):
        openWindow(self.parent, setSpectroMeterWindow, 'spectrometer')

    # --------------------------
    # Open the management window
    def callEquipmentManagement(self):
        openWindow(self.parent, manageEquipmentWindow, 'manage_equipment')

    # ---------------------------
    # Open the calibration window
    def callSyringeCalibrateWindow(self):
        openWindow(self.parent, calibrateSyringeWindow, 'calibrate_syringe')

    # ---------------------------
    # Open the calibration window
    def callTubingCalibrateWindow(self):
        openWindow(self.parent, calibrateTubingWindow, 'calibrate_tubing')

    # ---------------------------
    # Open the calibration window
    def callHeadsCalibrateWindow(self):
        openWindow(self.parent, calibrateHeadsWindow, 'calibrate_heads')

    # ---------------------------
    # Open the calibration window
    def callFlowmeterCalibrateWindow(self):
        openWindow(self.parent, calibrateFlowmeterWindow, 'calibrate_flowmeter')

    # ---------------------------
    # Open the calibration window
    def callPIDControllerCalibrateWindow(self):
        openWindow(self.parent, calibratePIDWindow, 'calibrate_pid')

    # ---------------------------
    # Open the calibration window
    def callGearboxCalibrateWindow(self):
        openWindow(self.parent, calibrateGearboxWindow, 'calibrate_gearbox')
