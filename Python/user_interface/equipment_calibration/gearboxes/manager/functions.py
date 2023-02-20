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

from settings.equipment.gearbox_calibration import getGearboxesInfos, deleteGearboxType

from user_interface._custom_widgets.icon_buttons import IconButton

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.notifications import warningProceedMessage
from user_interface.equipment_calibration.gearboxes.editor.display import editGearboxCalibrationWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class calibrateGearboxFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, name, content):

        # Fill the rows
        self.gearboxTable.insertRow(i)

        # Make the buttons
        gearboxEditButton = IconButton(icon_size=30, icon='settings_button.png')
        gearboxEditButton.released.connect(partial(self.editGearbox, gearbox_name=name))
        gearboxEditButton.setToolTip("Edit the settings of the gearbox.")

        gearboxDeleteButton = IconButton(icon_size=30, icon='delete_button.png')
        gearboxDeleteButton.released.connect(partial(self.deleteGearbox, gearbox_name=name))
        gearboxDeleteButton.setToolTip("Delete the gearbox.")

        # Fill the columns
        self.gearboxTable.setItem(i, 0,  qtw.QTableWidgetItem( name ))
        self.gearboxTable.setCellWidget(i, 1, gearboxEditButton)
        self.gearboxTable.setCellWidget(i, 2, gearboxDeleteButton)

        self.gearboxTable.setItem(i, 3,  qtw.QTableWidgetItem( '1:' + str(content['ratio']) ))
        self.gearboxTable.setItem(i, 4,  qtw.QTableWidgetItem( str(content['calibration_factor']) ))

    # ------------------
    # Populate the table
    def fillGearboxTable(self):

        # Get the list of trackers
        all_syringes = getGearboxesInfos()
        self.syringe_list = [ x for x in all_syringes.keys() ]

        # Reinialise the table
        self.gearboxTable.reset()

        # Fill the table
        i = -1
        if len(self.syringe_list) > 0:
            for i, name in enumerate(self.syringe_list):
                self._make_row(i, name, all_syringes[name])

        # Resize the columns
        self.gearboxTable.resizeCols()

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ---------------------------
    # Delete the selected gearbox
    def deleteGearbox(self, gearbox_name='untitled'):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the gearbox?','Are you sure you want to delete the selected gearbox? All its calibration will be lost.'):

            # Delete the selection
            deleteGearboxType(gearbox_name)

            # Reload the table
            self.fillGearboxTable()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------------
    # Modify the selected gearbox
    def editGearbox(self, gearbox_name=None):
        openWindow(self.parent, editGearboxCalibrationWindow, 'edit_gearbox', calibration_manager=self, gearbox_name=gearbox_name)
