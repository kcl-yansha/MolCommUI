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

from settings.equipment.syringe_calibration import getSyringeTypeList

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------
# Convert the volume
def _unit_to_steps(in_value, unit, syringe_area, microsteps=16):

    if unit == 'mm':
        temp_value = in_value

    elif unit == 'mL':
        temp_value = in_value * 1000 / syringe_area

    elif unit == 'µL':
        temp_value = in_value / syringe_area

    # Convert into spins
    out_value = temp_value / 0.8 * 200 * microsteps

    return out_value

# ----------------
# Convert the time
def _unit_to_time(in_value, unit):

    # Initialise the result
    out_value = in_value

    if unit == 's':
        out_value = in_value

    elif unit == 'min':
        out_value = in_value / 60.

    elif unit == 'h':
        out_value = in_value / 60. / 60.

    return out_value

# ----------------
# Convert the time
def _time_to_unit(in_value, unit):

    # Initialise the result
    out_value = in_value

    if unit == 's':
        out_value = in_value

    elif unit == 'min':
        out_value = in_value * 60.

    elif unit == 'h':
        out_value = in_value * 60. * 60.

    return out_value

# -----------------------------
# Convert speed to another unit
def _speed_to_basis(in_value, unit):

    # Split the unit
    volume, time = unit.split('/')

    # Convert the volume
    if volume == 'L':
        temp_value = in_value

    elif volume == 'mL':
        temp_value = in_value / 1000

    elif volume == 'µL':
        temp_value = in_value / 1000 / 1000

    # Convert the time
    out_value = _unit_to_time(temp_value, time)

    return out_value

# -----------------------------
# Convert speed to another unit
def _basis_to_speed(in_value, unit):

    # Split the unit
    volume, time = unit.split('/')

    # Convert the volume
    if volume == 'L':
        temp_value = in_value

    elif volume == 'mL':
        temp_value = in_value * 1000

    elif volume == 'µL':
        temp_value = in_value * 1000 * 1000

    # Convert the time
    out_value = _time_to_unit(temp_value, time)

    return out_value

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------
# Get the volume to inject
def getVolume(in_volume, unit, syringe_area, microsteps=16):

    # Split the unit
    volume, _ = unit.split('/')

    # Convert the volume into steps
    out_volume = _unit_to_steps(in_volume, volume, syringe_area, microsteps=microsteps)

    return out_volume

# ---------------------------
# Get the value for the speed
def getSpeed(in_speed, unit, syringe_area, microsteps=16):

    # Get the volume to displace
    out_speed = getVolume(in_speed, unit, syringe_area, microsteps=microsteps)

    # Split the unit
    _, time = unit.split('/')

    # Convert the time
    out_speed = _unit_to_time(out_speed, time)

    return out_speed

# ----------------------------------
# Get the value for the acceleration
def getAcceleration(in_accel, unit, syringe_area, microsteps=16):

    # Get the section area of the syringe
    out_accel = getSpeed(in_accel, unit, syringe_area, microsteps=microsteps)

    # Split the unit
    _, time = unit.split('/')

    # Convert the time
    out_accel = _unit_to_time(out_accel, time) # Call it twice to match the time unit

    return out_accel

# ---------------------------
# Convert the speed to uL/min
def speedToUlMin(value, unit):

    # Convert to basis speed
    temp_value = _speed_to_basis(value, unit)

    # Convert to uL/min
    out_value = _basis_to_speed(temp_value, 'µL/min')

    return out_value

# ---------------------------
# Convert the speed to uL/min
def uLminToSpeed(value, unit):

    # Convert to basis speed
    temp_value = _speed_to_basis(value, 'µL/min')

    # Convert to uL/min
    out_value = _basis_to_speed(temp_value, unit)

    return out_value
