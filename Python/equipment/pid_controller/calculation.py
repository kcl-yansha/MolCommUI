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

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------
# Get the flowrate
def _get_flow_rate(pid_controller, flowmeter_object, pump_objects):

    # CONDITIONS TO INTERRUPT THE SPEED CHECK
    # Are the pumps running?
    if pid_controller.full_speed == 0 or len(pump_objects) == 0:
        [x.resetFeedback() for x in pump_objects]
        return False, 0.

    # CONDITIONS TO INTERRUPT THE SPEED CHECK
    # Are the pumps still updating?
    pump_statuses = [x.is_updated for x in pump_objects]
    if not all(pump_statuses):
        return False, 0.

    # Get the flow speed
    crt_time, crt_flowrate = flowmeter_object.last_value

    # Initialise the previous time if required
    if pid_controller.prev_time is None:
        pid_controller.prev_time = crt_time - (flowmeter_object.delay / 1000)

    # Return the flowrate
    return True, abs(crt_flowrate)

# ---------------------------------------------
# Compute the new speed to apply to the syringe
def _compute_new_speed(pid_controller, flowrate_correction, pump_objects):

    # Get the total speed of the pumps
    total_speed = np.sum([x.speed for x in pump_objects])

    # Get the sign of the speed
    sign_speed = np.prod([np.sign(x.set_speed_ulmin) for x in pump_objects if x.set_speed_ulmin != 0])

    # Set the new speed
    new_speed = total_speed + flowrate_correction * sign_speed

    # Check if the two have the same sign
    set_speed = np.sum( [x.set_speed for x in pump_objects] )
    if new_speed * set_speed < 0:
        new_speed = total_speed / 2 # Reduce the speed if the correction change the speed sign

    # Calculate the value for all pumps
    all_speeds = []
    for pump in pump_objects:
        all_speeds.append( new_speed * pump.set_speed_ulmin / pid_controller.full_speed )

    return all_speeds

# ------------------------------------
# Calculate the new speed for the pump
def _pump_correction(pid_controller, flowrate, pump_objects, flowmeter_object):

    # Compute the error value
    error = abs(pid_controller.full_speed) - flowrate

    # Get the time step
    delta_t = flowmeter_object.last_value[0] - pid_controller.prev_time

    # Compute the different elements
    p_value = _get_Pvalue(pid_controller, error)
    i_value = _get_Ivalue(pid_controller, error, delta_t)
    d_value = _get_Dvalue(pid_controller, error, delta_t)

    # Calculate the correction value
    flowrate_correction = p_value + i_value + d_value

    # Get the new speed
    new_speed = _compute_new_speed(pid_controller, flowrate_correction, pump_objects)

    # Save the current values
    pid_controller.prev_time = flowmeter_object.last_value[0]
    pid_controller.prev_error = error

    return new_speed, np.array([error, p_value, i_value, d_value])

##-\-\-\-\-\
## PID VALUES
##-/-/-/-/-/

""" Code taken from:
https://en.wikipedia.org/wiki/PID_controller#Discrete_implementation
"""

# ------------------------------
# Get the proportional component
def _get_Pvalue(pid_controller, error):

    return pid_controller.p_value * error

# ----------------------------
# Get the integrated component
def _get_Ivalue(pid_controller, error, delta_t):

    # Calculate the integrated value
    pid_controller.prev_Ivalue += error * delta_t

    # Calculate the new term
    new_i_value = pid_controller.i_value * pid_controller.prev_Ivalue

    return new_i_value

# ---------------------------
# Get the derivated component
def _get_Dvalue(pid_controller, error, delta_t):

    # Calculate the derivated value
    derivative = (error - pid_controller.prev_error) / delta_t

    # Calculate the new value
    new_d_value = pid_controller.d_value * derivative

    return new_d_value

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------------
# Check if the current speed needs to be corrected
def speed_correction(pid_controller, flowmeter_object, pump_objects):

    # Get the flow speed
    is_new_value, crt_flowrate = _get_flow_rate(pid_controller, flowmeter_object, pump_objects)

    # Interrupt if no new value from flowmeter
    if not is_new_value:
        return False, [], []

    # Apply the PID correction on all pumps
    new_speeds, pid_values = _pump_correction(pid_controller, crt_flowrate, pump_objects, flowmeter_object)

    return True, new_speeds, pid_values
