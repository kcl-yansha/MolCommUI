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

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------------------------
# Get the information on the flow meter type(s)
def getFlowMeterType(return_list = False):

    # Define the types
    type_list = {

    # Sensirion SLI-0430
    'SLI-0430':{
    'chip':'SF04',
    'scale_factor': 270,
    'min_range':1,
    'max_range':120,
    'unit':'µL/min'
    },

    # Sensirion SLF3S-0600
    'SLF3S-0600':{
    'chip':'SF06',
    'scale_factor': 10,
    'min_range':1,
    'max_range':2000,
    'unit':'µL/min'
    },

    }

    # Return the list if required
    if return_list:
        return list(type_list.keys())

    else:
        return type_list
