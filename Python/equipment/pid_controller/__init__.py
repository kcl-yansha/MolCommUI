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

import numpy as np

from equipment.pid_controller.calculation import speed_correction

from settings.equipment.pid_calibration import loadPIDCalibrationConfig

##-\-\-\-\-\-\-\-\-\-\
## PID CONTROLLER CLASS
##-/-/-/-/-/-/-/-/-/-/

class PIDController:

    def __init__(self):

        # Equipment and values
        self.sensor = None
        self.motors = []

        self.all_speeds = {}
        self.full_speed = 0.

        # Controler parameters
        self.controller = None
        self.p_value = 0.
        self.i_value = 0.
        self.d_value = 0.

        # Integration and Derivative saved values
        self.resetMemory()

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Set the values of the PID controller
    def setPIDvalues(self, pid_dict):

        # Get the PID values
        self.controller = None
        self.p_value = pid_dict['p_coeff']
        self.i_value = pid_dict['i_coeff']
        self.d_value = pid_dict['d_coeff']

    # -------------------------------------
    # Get data from the PID controller type
    def updateType(self, new_controller=None):

        if new_controller is not None:

            # Extract the gearbox type
            controller_properties = loadPIDCalibrationConfig(new_controller)

            # Get the PID values
            self.controller = new_controller
            self.p_value = controller_properties['p_coeff']
            self.i_value = controller_properties['i_coeff']
            self.d_value = controller_properties['d_coeff']

    # ------------------------------
    # Reset the feedback loop memory
    def resetMemory(self):

        # Restore the values
        self.prev_error = 0.
        self.prev_time = None
        self.prev_Ivalue = 0.

    ##-\-\-\-\-\
    ## CORRECTION
    ##-/-/-/-/-/

    # -------------------------------------------------
    # Check the connection of the sensor and all motors
    def checkConnection(self):
        return self.sensor is not None and len(self.motors) != 0

    # ------------------------------
    # Get the correction if required
    def getCorrection(self):

        # Check if the connection is on before proceeding
        if self.checkConnection():

            # Get the new speed value
            to_update, new_speeds, pid_datas = speed_correction(self, self.sensor, self.motors)

            if to_update:
                for pump, speed in zip(self.motors, new_speeds):

                    # Set the new speed
                    pump.is_updated = False
                    pump.editSpeed(speed)

                    # Change the speed of the pump
                    pump.equipment.setSpeed(pid_data=pid_datas)

    ##-\-\-\-\-\
    ## CONNECTION
    ##-/-/-/-/-/

    # -------------------------
    # Add the speed to the list
    def addSpeed(self, pump, speed):

        # Add the pump to the list
        if pump not in self.motors:
            self.motors.append(pump)
        self.all_speeds[pump] = speed

        # Compute the new full speed
        return self.getFullSpeed()

    # ------------------------------
    # Remove the speed from the list
    def deleteSpeed(self, pump):

        # Remove the pump from the dictionary
        if pump in self.motors:
            self.motors.remove(pump)
        self.all_speeds.pop(pump, None)

        # Compute the new full speed
        return self.getFullSpeed()

    # ----------------------
    # Compute the full speed
    def getFullSpeed(self):
        self.full_speed = np.sum( [self.all_speeds[x] for x in self.all_speeds.keys()] )

        return self.full_speed
