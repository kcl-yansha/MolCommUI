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
from settings.general.manage_settings import getSections, config2dict

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------------------
# Get the default dictionary for the syringe settings
def _default_syringe_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    # General
    'type':'syringe',
    'syringe':'BD 1 mL',
    'gearbox':'No Gearbox',
    # Settings
    'speed':0.1,
    'speed_unit':'mm/s',
    'acceleration':1.0
    }

    # Return the required key
    if key is not None:
        return default_dict[key]

    # Return the whole dictionary
    else:
        return default_dict

# -------------------------------------------------
# Get the default dictionary for the group settings
def _default_group_dictionary(key=None):

    # Get the initial dictionary
    default_dict = {
    'type':'group',
    'X':'Syringe X',
    'Y':'Syringe Y',
    'Z':'Syringe Z',
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
    config['Syringe'] = _default_syringe_dictionary()

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    writeConfigFile(config, file_path)

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_group_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['Syringe Group'] = _default_group_dictionary()
    config['Syringe X'] = _default_syringe_dictionary()
    config['Syringe Y'] = _default_syringe_dictionary()
    config['Syringe Z'] = _default_syringe_dictionary()

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    writeConfigFile(config, file_path)

# -------------------------
# Open the user config file
def _open_config_path(file_name='defaultuser_syringes.ini'):

    # Get the path to the config file
    file_path = getSystemConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    if not os.path.exists(file_path):
        _init_default_group_config(file_path=file_path)

    return file_path

# ---------------------------------
# Add the new section to the config
def _add_config(configs, new_config_name, new_config_dict):

    # Add a syringe group
    if new_config_dict['type'] == 'group':

        # Process all the axes
        for axis in [x for x in ['x','y','z'] if x in new_config_dict.keys()]:

            # Extract the dictionary and name
            pump_dict = new_config_dict.pop(axis)
            pump_name = pump_dict.pop('name')

            # Add to the config
            configs[pump_name] = pump_dict

            # Replace the syringe name in the dict
            new_config_dict[axis.upper()] = pump_name

        # Add the group
        configs[new_config_name] = new_config_dict

    # Add a single syringe
    else:
        configs[new_config_name] = new_config_dict

    return configs

# ------------------
# Extract the config
def _extract_config(configs, item):

    # Check the type of the item
    config_dict = dict(configs.items(item))

    # Extract a syringe group
    if config_dict['type'] == 'group':

        # Loop over all syringes
        for key in [x for x in config_dict.keys() if x != 'type']:

            # Get the syringe name
            crt_name = config_dict[key]

            # Get the attributes
            config_dict[key] = dict(configs.items( crt_name ))
            config_dict[key]['name'] = crt_name

    # Add the name
    config_dict['name'] = item

    return config_dict

# ------------------------
# Get the type of the file
def _get_file_config(configs):

    # Get all the sections
    section_list = list(configs.sections())

    # Refine selection if is a syringe group
    if len(section_list) > 1:
        section_list = getSections(configs, search={'type':'group'})

    return section_list[0]

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------
# Get the list of syringe pump from the file
def getSyringeList(user_name='Default user', object_type = 'syringe'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_syringes.ini')
    config_content = openConfigFile(config_path)

    # Retrieve the sections
    syringe_list = getSections(config_content, search={'type':object_type})

    return syringe_list

# -----------------------------------------------------
# Save the syringe group config in the user config file
def saveSyringeGroupConfig(config_name, config_dict, user_name='Default user'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_syringes.ini')
    config_content = openConfigFile(config_path)

    # Add the new config
    config_content = _add_config(config_content, config_name, config_dict)

    # Write the config file
    writeConfigFile(config_content, config_path)

# -------------------------------------------
# Save the syringe group config in a new file
def saveSyringeGroupFile(config_name, config_dict, config_path):

    # Initialise the parser
    config = configparser.RawConfigParser()

    # Add the new config
    config = _add_config(config, config_name, config_dict)

    # Write the config file
    writeConfigFile(config, config_path)

# ---------------------------
# Load the configuration file
def loadSyringeGroupConfig(config_name, user_name='Default user'):

    # Convert the username
    user_name = user_name.lower().replace(' ','')
    config_path = _open_config_path(file_name=user_name+'_syringes.ini')
    config_content = openConfigFile(config_path)

    # Extract the config
    syringe_config = _extract_config(config_content, config_name)

    return syringe_config

# ---------------------------
# Load the configuration file
def loadSyringeGroupFile(config_path):

    # Convert the username
    config_content = openConfigFile(config_path)

    # Get the content of the file to load
    config_to_load = _get_file_config(config_content)

    # Extract the config
    syringe_config = _extract_config(config_content, config_to_load)

    return syringe_config
