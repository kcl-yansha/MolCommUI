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

import configparser
import os

from input_output.folder_management import createFolder
from settings.general.config_files_handling import getSystemConfigPath, openConfigFile, writeConfigFile, editSingleValue, removeSection
from settings.general.manage_settings import getSections, config2dict, checkValues

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -----------------------------------------------------
# Get the default dictionary for the flowmeter settings
def _default_flowmeter_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    # General
    'type':'SLF3S-0600',
    # Settings
    'calibration_factor':1.,
    }

    # Return the required key
    if key is not None:
        return default_dict[key]

    # Return the whole dictionary
    else:
        return default_dict

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_flowmeter_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    writeConfigFile(config, file_path)

# -------------------------
# Open the user config file
def _open_config_path(file_name='flowmeter_types.ini'):

    # Get the path to the config file
    file_path = getSystemConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    return file_path, os.path.exists(file_path)

# ---------------------------------
# Add the new section to the config
def _add_config(configs, new_config_name, new_config_dict):

    # Add a syringe config
    configs[new_config_name] = new_config_dict

    return configs

# ------------------
# Extract the config
def _extract_config(configs, item):

    # Check the type of the item
    config_dict = dict(configs.items(item))

    return config_dict

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------------
# Return the default calibration dictionary
def getDefaultCalibration():
    return _default_flowmeter_dictionary()

# -----------------------------
# Delete the selected flowmeter
def deleteFlowmeterType(config_name, file_name='flowmeter_types.ini'):

    # Get the path
    config_path, _ = _open_config_path(file_name=file_name)

    # Delete the object
    removeSection(config_path, config_name)

# ------------------------------------------
# Get the list of syringe pump from the file
def getSyringeTypeList(file_name='flowmeter_types.ini'):

    # Extract the config file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Retrieve the sections
    syringe_list = getSections(config_content)

    return syringe_list

# -----------------------------------------------
# Get all the infos of syringe pump from the file
def getFlowmeterTypeInfos(file_name='flowmeter_types.ini'):

    # Extract the config file
    config_path, config_exist = _open_config_path(file_name=file_name)

    if config_exist:
        config_content = openConfigFile(config_path)

        # Retrieve the sections
        flowmeter_list = config2dict(config_content)

        # Check the content
        for flowmeter_name in flowmeter_list.keys():
            flowmeter_list[flowmeter_name] = checkValues(flowmeter_list[flowmeter_name], _default_flowmeter_dictionary())

    else:
        flowmeter_list = {}

    return flowmeter_list

# -------------------------------------------------------------
# Save the flowmeter calibration config in the user config file
def saveFlowmeterConfig(config_name, config_dict, file_name='flowmeter_types.ini'):

    # Extract the config file
    config_path, config_exist = _open_config_path(file_name=file_name)

    # Generate a config if None are found
    if not config_exist:
        _init_default_flowmeter_config(config_path)

    # Open the content of the file
    config_content = openConfigFile(config_path)

    # Add the new config
    config_content = _add_config(config_content, config_name, config_dict)

    # Write the config file
    writeConfigFile(config_content, config_path)

# ---------------------------
# Load the configuration file
def loadFlowmeterCalibrationConfig(config_name, file_name='flowmeter_types.ini'):

    # Extract the config file
    config_path, config_exist = _open_config_path(file_name=file_name)

    if config_exist:
        config_content = openConfigFile(config_path)

        # Extract the config
        config_dict = _extract_config(config_content, config_name)

        # Check the content of the folder
        config_dict = checkValues(config_dict, _default_flowmeter_dictionary())

    else:
        config_dict = {}

    return config_dict
