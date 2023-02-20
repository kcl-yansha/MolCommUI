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

from user_interface._custom_widgets.icon_buttons import IconButton

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.notifications import warningProceedMessage
from user_interface.equipment_calibration.syringes.editor.display import editSyringeCalibrationWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class synchroniseSyringeFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, name, crt_group):

        # Fill the rows
        self.groupTable.insertRow(i)

        # Make the buttons
        groupSyncBox = qtw.QCheckBox()
        groupSyncBox.setToolTip("Synchronise the group with the flowmeter.")

        # Append
        self.groupSyncList.append( groupSyncBox )

        # Check the information
        if crt_group.sync_flowmeter == self.flowmeter:
            groupSyncBox.setChecked( True )

        # Fill the columns
        self.groupTable.setCellWidget(i, 0, groupSyncBox)
        self.groupTable.setItem(i, 1,  qtw.QTableWidgetItem( name ))

    # ------------------
    # Populate the table
    def fillGroupTable(self):

        # Get the list of trackers
        self.group_list = self.parent.groupDisplay.listGroupInstances(sync_only=True)
        group_name = [ x.name for x in self.group_list ]

        # Reinialise the table
        self.groupTable.reset()

        self.groupSyncList = []
        self.groupEntryList = []

        # Fill the table
        i = -1
        for i, name in enumerate(group_name):
            self._make_row(i, name, self.group_list[i])

        # Resize the columns
        self.groupTable.resizeCols()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------------
    # Synchronisation the selected syringe
    def setSynchronisation(self):

        # Process all the syringe
        for i, checkbox in enumerate(self.groupSyncList):

            # Synchronise
            if checkbox.isChecked():
                self.group_list[i].sync_flowmeter = self.flowmeter

            # Desynchronise
            else:
                if self.group_list[i].sync_flowmeter == self.flowmeter:
                    self.group_list[i].sync_flowmeter = None

        # Close the window
        self.close()
