import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.window_handling import openWindow

from user_interface.equipment_config.syringe_pump.arduino_group.display import setArduinoGroupWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class connectEquipmentFunctions(object):

    # --------------------------
    # Open the connection window
    def startConnectionMenu(self):

        # Open the new window
        openWindow(self.parent, setArduinoGroupWindow, 'arduino_group')

        # Close the current one
        self.close()
