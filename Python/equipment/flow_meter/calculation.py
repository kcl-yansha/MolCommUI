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

# ---------------------------------------------
# Add the value to the array of previous values
def _add_to_previous(new_value, flowmeter_object):

    # Get the values and add the new value
    prev_values = flowmeter_object.previous_values
    prev_values.append(new_value)

    # Remove old values if needed
    n_extra = len(prev_values) - flowmeter_object.n_previous
    if n_extra > 0:
        prev_values = prev_values[ n_extra: ]

    # Save the list in the class
    flowmeter_object.previous_values = prev_values

    return prev_values

# ------------------------------
# Apply a running average filter
def _running_avg(all_values):
    return np.mean(all_values)

# ----------------
# Get the flowrate
def _get_flow_rate(flowmeter_object, pump_objects):

    # CONDITIONS TO INTERRUPT THE SPEED CHECK
    # Are the pumps running?
    if flowmeter_object.full_speed == 0 or len(pump_objects) == 0:
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
    if flowmeter_object.pid_prev_time is None:
        flowmeter_object.pid_prev_time = crt_time - (flowmeter_object.delay / 1000)

    # Return the flowrate
    return True, abs(crt_flowrate)

# ---------------------------------------------
# Compute the new speed to apply to the syringe
def _compute_new_speed(flowrate_correction, pump_objects, flowmeter_object):

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
        all_speeds.append( new_speed * pump.set_speed_ulmin / flowmeter_object.full_speed )

    return all_speeds

# ------------------------------------
# Calculate the new speed for the pump
def _pump_correction(flowrate, pump_objects, flowmeter_object):

    # Rescale the flowrate by the contribution of the pump to the total flowrate
    #flowrate = flowrate * pump_object.set_speed_ulmin / flowmeter_object.full_speed

    # Compute the error value
    error = abs(flowmeter_object.full_speed) - flowrate

    # Get the time step
    delta_t = flowmeter_object.last_value[0] - flowmeter_object.pid_prev_time

    # Compute the different elements
    p_value = _get_Pvalue(error, flowmeter_object)
    i_value = _get_Ivalue(error, flowmeter_object, delta_t)
    d_value = _get_Dvalue(error, flowmeter_object, delta_t)

    # Calculate the correction value
    flowrate_correction = p_value + i_value + d_value

    # Get the new speed
    new_speed = _compute_new_speed(flowrate_correction, pump_objects, flowmeter_object)

    # Save the current values
    flowmeter_object.pid_prev_time = flowmeter_object.last_value[0]
    flowmeter_object.pid_prev_error = error

    return new_speed, np.array([error, p_value, i_value, d_value])

##-\-\-\-\-\
## PID VALUES
##-/-/-/-/-/

""" Code taken from:
https://en.wikipedia.org/wiki/PID_controller#Discrete_implementation
"""

# ------------------------------
# Get the proportional component
def _get_Pvalue(error, flowmeter_object):

    return flowmeter_object.pid_factor_p * error # From Wikipedia v2.0

# ----------------------------
# Get the integrated component
def _get_Ivalue(error, flowmeter_object, delta_t):

    # Calculate the integrated value
    flowmeter_object.pid_prev_Ivalue += error * delta_t

    # Calculate the new term
    new_i_value = flowmeter_object.pid_factor_i * flowmeter_object.pid_prev_Ivalue

    return new_i_value

# ---------------------------
# Get the derivated component
def _get_Dvalue(error, flowmeter_object, delta_t):

    # Calculate the derivated value
    derivative = (error - flowmeter_object.pid_prev_error) / delta_t

    # Calculate the new value
    new_d_value = flowmeter_object.pid_factor_d * derivative

    return new_d_value

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------
# Return the filtered value
def apply_filter(new_value, flowmeter_object):

    # Get the array to process
    all_values = _add_to_previous(new_value, flowmeter_object)

    # Get the filtered value
    filtered_value = _running_avg(all_values)

    return filtered_value

# ------------------------------------------------
# Check if the current speed needs to be corrected
def speed_correction(flowmeter_object, pump_objects):

    # Get the flow speed
    is_new_value, crt_flowrate = _get_flow_rate(flowmeter_object, pump_objects)

    # Interrupt if no new value from flowmeter
    if not is_new_value:
        return False, [], []

    # Apply the PID correction on all pumps
    new_speeds, pid_values = _pump_correction(crt_flowrate, pump_objects, flowmeter_object)

    #set_speed = np.sum([x.set_speed_ulmin for x in pump_objects])
    #print('Set:',set_speed,'Measured:',crt_flowrate, 'New speeds:', new_speeds, 'PID:', pid_values)

    return True, new_speeds, pid_values
