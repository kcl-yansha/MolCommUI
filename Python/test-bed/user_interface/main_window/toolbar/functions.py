import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.connect_equipment.display import connectEquipmentWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class toolBarFunctions(object):

    # --------------------------
    # Open the connection window
    def callEquipmentConnectionWindow(self):
        openWindow(self.parent, connectEquipmentWindow, 'connect_equipment')
