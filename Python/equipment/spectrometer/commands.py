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
#------------------------------------------------------------#
# Note(s):                                                   #
# Codes adapted from the python-seabreeze Read the Docs      #
# website                                                    #
# Link: https://python-seabreeze.readthedocs.io/en/latest/   #
# Current version: v1.3.0                                    #
###========================================================###

from seabreeze.spectrometers import list_devices, Spectrometer

"""
Codes adapted from the python-seabreeze Read the Docs website
Link: https://python-seabreeze.readthedocs.io/en/latest/
Current version: v1.3.0
"""

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------------------
# Get the list of available spectrometers
def get_list_spectrometers():

    # Get the list of spectrometers serial numbers
    all_serial = [x.serial_number for x in list_devices()]

    return all_serial

# ----------------------------------------
# Start the connection to the spectrometer
def start_connection(serial_number):

    # Connect to the spectrometer
    spectro_unit = Spectrometer.from_serial_number(serial_number)

    return spectro_unit

# ---------------------------------------
# Stop the connection to the spectrometer
def stop_connection(spectro_unit):
    spectro_unit.close()

# ----------------------------------------
# Get the main details of the spectrometer
def get_spectrometer_infos(spectro_unit):

    # Build the dictionary
    spectro_dict = {
    'model':spectro_unit.model,
    'pixels':spectro_unit.pixels
    }

    return spectro_dict

# --------------------------------------------
# Set the integration time of the spectrometer
def set_integration_time(spectro_unit, time_value, debug=False):

    # Update the value
    spectro_unit.integration_time_micros(time_value)

    # Be verbose
    if debug:
        print('Spectrometer',spectro_unit.serial_number,'set integration time to',time_value/1000,'ms')

# ------------------
# Make a measurement
def get_measurement(spectro_unit, intensity_only=True, debug=False):

    # Extract the values
    if intensity_only:
        signal = spectro_unit.intensities()
    else:
        signal = spectro_unit.spectrum()

    # Be verbose
    if debug:
        print('Spectrometer',spectro_unit.serial_number,'measured array of size',signal.shape)

    return signal
