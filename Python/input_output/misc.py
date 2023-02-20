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

from datetime import datetime

import PyQt5.QtCore as qtc

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------------------
# Convert the date instance into a string
def date2str(date_object):

    # Process QDateTime instances
    if isinstance(date_object, qtc.QDateTime):
        date_text = date_object.toString('yyyy/MM/dd, hh:mm:ss')

    # Processe datetime instances
    else:
        date_text = date_object.strftime("%Y/%m/%d, %H:%M:%S")

    return date_text

# ------------------------------------------------
# Convert a string into the selected date instance
def str2date(date_text, qt=False):

    # Transform into a QDateTime instance
    if qt:
        date_object = qtc.QDateTime.fromString(date_text, 'yyyy/MM/dd, hh:mm:ss')

    else:
        date_object = datetime.strptime(date_text, "%Y/%m/%d, %H:%M:%S")

    return date_object
