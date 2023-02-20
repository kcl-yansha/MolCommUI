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

from input_output.folder_management import createFolder

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -------------------------------
# Convert the array into a string
def _array2str(array, delimiter=','):

    # Add single line
    if len(array.shape) == 1:

        # Loop over all elements
        str_txt = str(array[0])
        for item in array[1:]:
            str_txt += delimiter + str(item)

        # Jump line
        str_txt += '\n'

    # Add multiple lines
    else:

        # Loop over all rows
        str_txt = ""
        for row in array:
            str_txt += str(row[0])

            # Loop over all elements
            for item in row[1:]:
                str_txt += delimiter + str(item)

            # Jump line
            str_txt += '\n'

    return str_txt

# -------------------
# Initialise the file
def _init_file(path, head=None, delimiter=','):

    # Check if the folder needs to be created
    folder_name = os.path.dirname(path)
    if not os.path.exists( folder_name ):
        createFolder(path)

    # Open the file
    f = open(path, 'w')

    # Check if header is provided
    if head is not None:

        # Add the comments
        if len(head['comments']) > 0:
            for comment in head['comments']:
                f.write( '# ' + comment + '\n' )

        # Add the header
        col_txt = head['header'][0]
        for col in head['header'][1:]:
            col_txt += delimiter + col
        col_txt += '\n'

        f.write(col_txt)

    # Save the file
    f.close()

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------------
# Write the content to the selected file
def write2file(path, array, head=None, delimiter=','):

    # Initialise the file if it does not exist
    if not os.path.isfile(path):
        _init_file(path, head=head, delimiter=delimiter)

    # Format the array in a string
    new_text = _array2str(array, delimiter=delimiter)

    # Append the array to the file
    f = open(path, 'a')
    f.write(new_text)
    f.close()
