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

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## DEFINE THE MAIN EQUIPMENT CLASS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class Equipment:
    def __init__(self, etype):

        # Define the general parameters
        self.type = etype
