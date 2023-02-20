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

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# --------------------------------
# Search the dictionary for values
def _search_and_check(section_dict, search_dict):

    # Loop all the elements
    for key, value in search_dict.items():

        # Search if the key exist
        if key not in section_dict.keys():
            return False

        else:
            # Check if the value corresponds
            if section_dict[key] != value:
                return False

    return True

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------
# Get the list of sections
def getSections(configs, exclude='MAIN', search=None):

    # Initialise the list
    section_list = []

    # Make the list
    for section in configs.sections():

        # Turn the config into a dictionary
        section_dict = dict(configs.items(section))

        # Check that any search condition is met
        _is_checked = True
        if search is not None:
            _is_checked = _search_and_check(section_dict, search)

        # Add the section to the list if allowed
        if section != exclude and _is_checked:
            section_list.append(section)

    return section_list

# ------------------------------------------
# Convert a config content into a dictionary
def config2dict(configs):

    # Process all sections
    conf_dict = {}
    for section in configs.sections():

        # Initialise the section dictionary
        conf_dict[section] = {}

        # Process all subsections
        for subsection in configs[section]:
            conf_dict[section][subsection] = configs[section][subsection]

    return conf_dict

# ------------------------------------
# Convert a config content into a list
def config2list(configs):

    # Process all sections
    conf_dict = {}
    for section in configs.sections():

        # Process all subsections
        for subsection in configs[section]:
             conf_dict[int(subsection)] = configs[section][subsection]

    # Get and sort the keys
    conf_indices = list(conf_dict.keys())
    conf_indices.sort()

    # Make the list
    conf_list = []
    for key in conf_indices:
        conf_list.append( conf_dict[key] )

    return conf_list

# -------------------------------------------------
# Check the loaded dictionary for incomplete values
def checkValues(loaded_dict, default_dict):

    # Loop over all the values in the default dict
    for setting in default_dict.keys():

        # Add the default value if missing
        if setting not in loaded_dict.keys():
            loaded_dict[ setting ] = default_dict[ setting ]

        # Check the type
        else:

            # Format boolean
            if isinstance(default_dict[ setting ], bool):
                loaded_dict[ setting ] = loaded_dict[ setting ] == 'True'

            elif isinstance(default_dict[ setting ], int):
                loaded_dict[ setting ] = int( loaded_dict[ setting ] )

            elif isinstance(default_dict[ setting ], float):
                loaded_dict[ setting ] = float( loaded_dict[ setting ] )

    return loaded_dict
