##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## DEFINE THE MAIN EQUIPMENT CLASS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class Equipment:
    def __init__(self, etype, instance, **kwargs):

        # Define the general parameters
        self.type = etype

        # Set the equipment based on its type
        if self.type == 'syringe_pump':

            # Get the required arguments
            axis = kwargs.get('axis_port','X')

            # Load the syringe
            self.setSyringe(instance, axis_port=axis)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## ADD THE INSTANCE OF THE EQUIPMENT
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------
    # Set a syringe
    def setSyringe(self, instance, axis_port='X'):

        # Save the equipment
        self.equipment = instance.syringes[ axis_port ]
        self.name = self.equipment.name
        self.syringe_group = instance
