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

from functools import partial

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from settings.equipment.pid_calibration import getPIDInfos, deletePIDController

from user_interface._custom_widgets.icon_buttons import IconButton

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.notifications import warningProceedMessage
from user_interface.equipment_calibration.pid_controllers.editor.display import editPIDCalibrationWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class calibratePIDFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, name, content):

        # Fill the rows
        self.controllerTable.insertRow(i)

        # Make the buttons
        controllerEditButton = IconButton(icon_size=30, icon='settings_button.png')
        controllerEditButton.released.connect(partial(self.editController, controller_name=name))
        controllerEditButton.setToolTip("Edit the settings of the PID controller.")

        controllerDeleteButton = IconButton(icon_size=30, icon='delete_button.png')
        controllerDeleteButton.released.connect(partial(self.deleteController, controller_name=name))
        controllerDeleteButton.setToolTip("Delete the PID controller.")

        # Fill the columns
        self.controllerTable.setItem(i, 0,  qtw.QTableWidgetItem( name ))
        self.controllerTable.setCellWidget(i, 1, controllerEditButton)
        self.controllerTable.setCellWidget(i, 2, controllerDeleteButton)

        self.controllerTable.setItem(i, 3,  qtw.QTableWidgetItem( str(content['p_coeff']) ))
        self.controllerTable.setItem(i, 4,  qtw.QTableWidgetItem( str(content['i_coeff']) ))
        self.controllerTable.setItem(i, 5,  qtw.QTableWidgetItem( str(content['d_coeff']) ))

    # ------------------
    # Populate the table
    def fillControllerTable(self):

        # Get the list of trackers
        all_controller = getPIDInfos()
        self.controller_list = [ x for x in all_controller.keys() ]

        # Reinialise the table
        self.controllerTable.reset()

        # Fill the table
        i = -1
        if len(self.controller_list) > 0:
            for i, name in enumerate(self.controller_list):
                self._make_row(i, name, all_controller[name])

        # Resize the columns
        self.controllerTable.resizeCols()

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ------------------------------
    # Delete the selected controller
    def deleteController(self, controller_name='untitled'):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the controller?','Are you sure you want to delete the selected PID controller? All its calibration will be lost.'):

            # Delete the selection
            deletePIDController(controller_name)

            # Reload the table
            self.fillControllerTable()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------
    # Modify the selected controller
    def editController(self, controller_name=None):
        openWindow(self.parent, editPIDCalibrationWindow, 'edit_pid', calibration_manager=self, controller_name=controller_name)
