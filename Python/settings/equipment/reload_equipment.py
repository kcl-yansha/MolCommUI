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
from settings.general.config_files_handling import getSystemConfigPath, openConfigFile, writeConfigFile, editSingleValue
from settings.general.manage_settings import getSections, config2dict, checkValues

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------------------
# Get the default dictionary for the preloaded equipment
def _default_equipment_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    # General
    'enabled':True,
    }

    # Return the required key
    if key is not None:
        return default_dict[key]

    # Return the whole dictionary
    else:
        return default_dict

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_equipment_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['MAIN'] = _default_equipment_dictionary()

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    writeConfigFile(config, file_path)

# -------------------------
# Open the user config file
def _open_config_path(file_name='defaultuser_preload.ini'):

    # Get the path to the config file
    file_path = getSystemConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    if not os.path.exists(file_path):
        _init_default_equipment_config(file_path=file_path)

    return file_path

# ------------------
# Extract the config
def _extract_config(configs, item):

    # Check the type of the item
    config_dict = dict(configs.items(item))

    return config_dict

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------------------
# Change the status of the preloading in the config file
def togglePreload(status, user_name='Default user'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_preload.ini')
    config_content = openConfigFile(config_path)

    # Edit the value
    config_dict = _extract_config(config_content, 'MAIN')
    config_dict['enabled'] = status

    # Replace in the config
    config_content['MAIN'] = config_dict

    # Write the config file
    writeConfigFile(config_content, config_path)

# ---------------------------------------------------
# Get the list of equipment to pre-load from the file
def getEquipmentList(user_name='Default user'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_preload.ini')
    config_content = openConfigFile(config_path)

    # Check if enabled
    config_dict = _extract_config(config_content, 'MAIN')
    config_dict = checkValues(config_dict, _default_equipment_dictionary())
    is_enabled = config_dict['enabled']

    # Retrieve the sections
    equipment_list = getSections(config_content)

    return is_enabled, equipment_list

# -----------------------------
# Add a port to the config file
def addPort(port, port_dict, user_name='Default user'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_preload.ini')
    config_content = openConfigFile(config_path)

    # Add in the config
    config_content[port] = port_dict

    # Write the config file
    writeConfigFile(config_content, config_path)

# -----------------------------------------------------
# Get the details of the equipment on the selected port
def getPortInfos(port, user_name='Default user'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_preload.ini')
    config_content = openConfigFile(config_path)

    # Check if enabled
    config_dict = _extract_config(config_content, port)

    return config_dict
