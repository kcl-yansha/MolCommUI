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

import os

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------
# Create the selected folder
def createFolder(file_path):

    # Create all the directories if needed
    try:
        os.makedirs(os.path.dirname(file_path))

    # Guard against race condition
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

# --------------------------------------------------------
# Check if the folder already exists - append if necessary
def checkPreviousFolder(folder, exp_folder_name):

    # Get the path
    new_folder = os.path.join(folder, exp_folder_name)

    # Check if the folder already exists
    while os.path.isdir(new_folder):

        # Get the last element of the name
        all_elements = exp_folder_name.split('_')
        last_element = all_elements[-1]

        # Add the counter
        try:
            last_element = int(last_element) + 1

            exp_folder_name = all_elements[0]
            for element in all_elements[1:-1]:
                exp_folder_name += '_' + element

            exp_folder_name += '_' + str(last_element)

        except:
            exp_folder_name += '_1'

        # Re-make the path
        new_folder = os.path.join(folder, exp_folder_name)

    return new_folder
