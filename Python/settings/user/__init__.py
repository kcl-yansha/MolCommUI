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

# ------------------------------------------------
# Get the default dictionary for the main settings
def _default_main_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    # General
    'current_user':'Default User',
    # Debug
    'debug_syringe':True,
    'debug_syringe_send':False,
    'debug_flowmeter':False,
    'debug_valve':False,
    }

    # Return the required key
    if key is not None:
        return default_dict[key]

    # Return the whole dictionary
    else:
        return default_dict

# -------------------------------
# Get the user default dictionary
def _default_user_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    # General
    'save_folder': os.path.expanduser('~/Desktop') ,
    'use_date': True ,
    }

    # Return the required key
    if key is not None:
        return default_dict[key]

    # Return the whole dictionary
    else:
        return default_dict

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['MAIN'] = _default_main_dictionary()
    config['Default User'] = _default_user_dictionary()

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    writeConfigFile(config, file_path)

# -------------------------
# Open the user config file
def _open_config_path(file_name='config.ini'):

    # Get the path to the config file
    file_path = getSystemConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    if not os.path.exists(file_path):
        _init_default_config(file_path=file_path)

    return file_path

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------
# Retrieve the list of users
def getUserList(file_name='config.ini'):

    # Get the link to the main file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Retrieve the section
    user_lists = getSections(config_content)

    return user_lists

# --------------------
# Load the user config
def getUserConfig(user_name, file_name='config.ini'):

    # Get the link to the main file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Convert the config into a dictionary
    config_dict = config2dict(config_content)

    # Check the content of the folder
    config_dict_user = checkValues(config_dict[user_name], _default_user_dictionary())

    return config_dict_user

# ---------------------------------------
# Create a new user with default settings
def createNewUser(user_name, file_name='config.ini'):

    # Get the link to the main file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Add the default content for the user
    config_content[user_name] = _default_user_dictionary()

    # Save the file
    writeConfigFile(config_content, config_path)

# ---------------------------
# Load the configuration file
def loadMainConfig(file_name='config.ini'):

    # Get the link to the main file
    config_path = _open_config_path(file_name=file_name)
    config_content = openConfigFile(config_path)

    # Convert the config into a dictionary
    config_dict = config2dict(config_content)

    # Check the content of the folder
    config_dict = checkValues(config_dict['MAIN'], _default_main_dictionary())

    return config_dict

# --------------------------------------
# Edit a single value in the config file
def editUserConfigValue(section, key, value, file_name='config.ini'):

    # Get the link to the main file
    config_path = _open_config_path(file_name=file_name)

    # Edit the file
    editSingleValue(config_path, section, key, value)
