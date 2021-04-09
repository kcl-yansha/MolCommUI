##-\-\-\-\-\-\-\-\-\
## GENERAL PROPERTIES
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------
# Get the information on the syringe type(s)
def getSyringeType(return_list = False):

    # Define the types
    type_list = {
    'BD 1 mL':{},
    'BD 10 mL':{},
    }

    # Return the list if required
    if return_list:
        return list(type_list.keys())

    else:
        return type_list
