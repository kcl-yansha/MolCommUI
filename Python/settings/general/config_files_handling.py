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

from appdirs import AppDirs
import configparser
import os

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------
# Return the default folder of the system
def _return_default_folder():

    # Search the default directory of the system
    default_directory = AppDirs('Molecular-Communication', 'YanshaLab', version="1.0")
    default_directory = default_directory.user_data_dir

    return default_directory

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------------
# Return the path to the config file in the system
def getSystemConfigPath(file_name='config.ini'):

    # Get the path to the config file
    default_directory = _return_default_folder()
    file_path = os.path.join(default_directory, file_name)

    return file_path

# --------------------
# Open the config file
def openConfigFile(file_path):

    # Load the content of the file
    config = configparser.RawConfigParser()
    config.read(file_path)

    return config

# ---------------------
# Write the config file
def writeConfigFile(config, file_path):

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# ---------------------------------
# Edit the value in the config file
def editSingleValue(file_path, section, key, value):

    # Load the content of the file
    config = configparser.RawConfigParser()
    config.read(file_path)

    # Replace the value
    config.set(section, key, value)

    # Save the file
    writeConfigFile(config, file_path)

# -------------------------------------------
# Remove the selected section from the config
def removeSection(file_path, section):

    # Load the content of the file
    config = configparser.RawConfigParser()
    config.read(file_path)

    # Replace the value
    config.remove_section(section)

    # Save the file
    writeConfigFile(config, file_path)
