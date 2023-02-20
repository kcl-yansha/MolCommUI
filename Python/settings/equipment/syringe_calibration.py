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

# ---------------------------------------------------
# Get the default dictionary for the syringe settings
def _default_syringe_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    # General
    'volume':1.,
    'diameter':4.699,
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
def _init_default_syringe_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['BD 1 mL'] = _default_syringe_dictionary()

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    writeConfigFile(config, file_path)

# -------------------------
# Open the user config file
def _open_config_path(file_name='syringe_types.ini'):

    # Get the path to the config file
    file_path = getSystemConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    if not os.path.exists(file_path):
        _init_default_syringe_config(file_path=file_path)

    return file_path

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
    return _default_syringe_dictionary()

# ---------------------------
# Delete the selected syringe
def deleteSyringeType(config_name, file_name='syringe_types.ini'):

    # Get the path
    config_path = _open_config_path(file_name=file_name)

    # Delete the object
    removeSection(config_path, config_name)

# ------------------------------------------
# Get the list of syringe pump from the file
def getSyringeTypeList(file_name='syringe_types.ini'):

    # Extract the config file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Retrieve the sections
    syringe_list = getSections(config_content)

    return syringe_list

# -----------------------------------------------
# Get all the infos of syringe pump from the file
def getSyringeTypeInfos(file_name='syringe_types.ini'):

    # Extract the config file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Retrieve the sections
    syringe_list = config2dict(config_content)

    # Check the content
    for syringe_name in syringe_list.keys():
        syringe_list[syringe_name] = checkValues(syringe_list[syringe_name], _default_syringe_dictionary())

    return syringe_list

# -----------------------------------------------------------
# Save the syringe calibration config in the user config file
def saveSyringeGroupConfig(config_name, config_dict, file_name='syringe_types.ini'):

    # Extract the config file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Add the new config
    config_content = _add_config(config_content, config_name, config_dict)

    # Write the config file
    writeConfigFile(config_content, config_path)

# ---------------------------
# Load the configuration file
def loadSyringeCalibrationConfig(config_name, file_name='syringe_types.ini'):

    # Extract the config file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Extract the config
    config_dict = _extract_config(config_content, config_name)

    # Check the content of the folder
    config_dict = checkValues(config_dict, _default_syringe_dictionary())

    return config_dict
