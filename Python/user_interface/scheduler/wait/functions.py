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

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from multithreading.scheduler.events import Wait

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setWaitFunctions(object):

    ##-\-\-\-\-\-\-\
    ## INIT INTERFACE
    ##-/-/-/-/-/-/-/

    # ----------------------
    # Populate the interface
    def initInterface(self):

        if self.event is not None:

            # Apply all the values
            self.valueDuration.setValue( self.event.duration )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------
    # Edit the settings of the pulse
    def setWait(self):

        # Retrieve all the values
        duration = self.valueDuration.value()

        # Create a new event
        if self.event is None:

            # Create the new event
            new_event = Wait(duration)

            # Add to the list
            self.parent_widget.addEvent(new_event)

        # Edit the existing event
        else:

            # New values
            self.event.duration = duration

            # Regenerate the values
            self.event.getCommands()
            self.event.getDescription()

        # Refresh the display
        self.close()
        self.parent_widget.fillEventTable()
