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

from settings.equipment.syringe_calibration import getSyringeTypeInfos, deleteSyringeType

from user_interface._custom_widgets.icon_buttons import IconButton

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.notifications import warningProceedMessage
from user_interface.equipment_calibration.syringes.editor.display import editSyringeCalibrationWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class calibrateSyringeFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, name, content):

        # Fill the rows
        self.syringeTable.insertRow(i)

        # Make the buttons
        syringeEditButton = IconButton(icon_size=30, icon='settings_button.png')
        syringeEditButton.released.connect(partial(self.editSyringe, syringe_name=name))
        syringeEditButton.setToolTip("Edit the settings of the syringe.")

        syringeDeleteButton = IconButton(icon_size=30, icon='delete_button.png')
        syringeDeleteButton.released.connect(partial(self.deleteSyringe, syringe_name=name))
        syringeDeleteButton.setToolTip("Delete the syringe.")

        # Fill the columns
        self.syringeTable.setItem(i, 0,  qtw.QTableWidgetItem( name ))
        self.syringeTable.setCellWidget(i, 1, syringeEditButton)
        self.syringeTable.setCellWidget(i, 2, syringeDeleteButton)

        self.syringeTable.setItem(i, 3,  qtw.QTableWidgetItem( str(content['volume'])+' mL' ))
        self.syringeTable.setItem(i, 4,  qtw.QTableWidgetItem( str(content['diameter'])+' mm' ))
        self.syringeTable.setItem(i, 5,  qtw.QTableWidgetItem( str(content['calibration_factor']) ))

    # ------------------
    # Populate the table
    def fillSyringeTable(self):

        # Get the list of trackers
        all_syringes = getSyringeTypeInfos()
        self.syringe_list = [ x for x in all_syringes.keys() ]

        # Reinialise the table
        self.syringeTable.reset()

        # Fill the table
        i = -1
        if len(self.syringe_list) > 0:
            for i, name in enumerate(self.syringe_list):
                self._make_row(i, name, all_syringes[name])

        # Resize the columns
        self.syringeTable.resizeCols()

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ---------------------------
    # Delete the selected syringe
    def deleteSyringe(self, syringe_name='untitled'):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the syringe?','Are you sure you want to delete the selected syringe? All its calibration will be lost.'):

            # Delete the selection
            deleteSyringeType(syringe_name)

            # Reload the table
            self.fillSyringeTable()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------------
    # Modify the selected syringe
    def editSyringe(self, syringe_name=None):
        openWindow(self.parent, editSyringeCalibrationWindow, 'edit_syringe', calibration_manager=self, syringe_name=syringe_name)
