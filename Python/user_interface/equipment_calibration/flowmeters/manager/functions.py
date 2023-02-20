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

from settings.equipment.flowmeter_calibration import getFlowmeterTypeInfos, deleteFlowmeterType

from user_interface._custom_widgets.icon_buttons import IconButton

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.notifications import warningProceedMessage
from user_interface.equipment_calibration.flowmeters.editor.display import editFlowmeterCalibrationWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class calibrateFlowmeterFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, name, content):

        # Fill the rows
        self.flowmeterTable.insertRow(i)

        # Make the buttons
        flowmeterEditButton = IconButton(icon_size=30, icon='settings_button.png')
        flowmeterEditButton.released.connect(partial(self.editFlowmeter, flowmeter_serial=name))
        flowmeterEditButton.setToolTip("Edit the settings of the flowmeter.")

        flowmeterDeleteButton = IconButton(icon_size=30, icon='delete_button.png')
        flowmeterDeleteButton.released.connect(partial(self.deleteFlowmeter, flowmeter_serial=name))
        flowmeterDeleteButton.setToolTip("Delete the flowmeter.")

        # Fill the columns
        self.flowmeterTable.setItem(i, 0,  qtw.QTableWidgetItem( name ))
        self.flowmeterTable.setCellWidget(i, 1, flowmeterEditButton)
        self.flowmeterTable.setCellWidget(i, 2, flowmeterDeleteButton)

        self.flowmeterTable.setItem(i, 3,  qtw.QTableWidgetItem( str(content['type']) ))
        self.flowmeterTable.setItem(i, 4,  qtw.QTableWidgetItem( str(content['calibration_factor']) ))

    # ------------------
    # Populate the table
    def fillFlowmeterTable(self):

        # Get the list of trackers
        all_flowmeters = getFlowmeterTypeInfos()
        self.flowmeter_list = [ x for x in all_flowmeters.keys() ]

        # Reinialise the table
        self.flowmeterTable.reset()

        # Fill the table
        i = -1
        if len(self.flowmeter_list) > 0:
            for i, name in enumerate(self.flowmeter_list):
                self._make_row(i, name, all_flowmeters[name])

        # Resize the columns
        self.flowmeterTable.resizeCols()

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # -----------------------------
    # Delete the selected flowmeter
    def deleteFlowmeter(self, flowmeter_serial='untitled'):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the flowmeter?','Are you sure you want to delete the selected flowmeter? All its calibration will be lost.'):

            # Delete the selection
            deleteFlowmeterType(flowmeter_serial)

            # Reload the table
            self.fillFlowmeterTable()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------------------
    # Modify the selected flowmeter
    def editFlowmeter(self, flowmeter_serial=None):
        openWindow(self.parent, editFlowmeterCalibrationWindow, 'edit_flowmeter', calibration_manager=self, flowmeter_serial=flowmeter_serial)
