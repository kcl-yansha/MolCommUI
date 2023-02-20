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
from user_interface.equipment_config.syringe_pump.arduino_group.display import setArduinoGroupWindow
from user_interface.equipment_config.flow_meter.display import setFlowMeterWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class manageEquipmentFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, port):

        # Fill the rows
        self.equipmentsTable.insertRow(i)

        # Get the information from the dictionary
        equipment_type, equipment = self.equipment_list[port]

        # Make the buttons
        equipmentEditButton = IconButton(icon_size=30, icon='settings_button.png')
        equipmentEditButton.released.connect(partial(self.editEquipment, serial_port=port))
        equipmentEditButton.setToolTip("Edit the settings of the equipment.")

        equipmentDeleteButton = IconButton(icon_size=30, icon='delete_button.png')
        equipmentDeleteButton.released.connect(partial(self.deleteEquipment, serial_port=port))
        equipmentDeleteButton.setToolTip("Delete the equipment.")

        # Fill the columns
        self.equipmentsTable.setItem(i, 0,  qtw.QTableWidgetItem( equipment_type ))
        self.equipmentsTable.setItem(i, 1,  qtw.QTableWidgetItem( port ))
        self.equipmentsTable.setCellWidget(i, 2, equipmentEditButton)
        self.equipmentsTable.setCellWidget(i, 3, equipmentDeleteButton)

    # ------------------
    # Populate the table
    def fillEquipmentTable(self):

        # Fetch the equipment list
        self.equipment_list = self.parent.listEquipment()

        # Reinialise the table
        self.equipmentsTable.reset()

        # Fill the table
        for i, port in enumerate(self.equipment_list.keys()):
            self._make_row(i, port)

        # Resize the columns
        self.equipmentsTable.resizeCols()

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ---------------------------
    # Delete the selected syringe
    def deleteEquipment(self, serial_port=None):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the equipment?','Are you sure you want to delete the selected equipment? This will disconnect and empty the serial port.'):

            # Get the equipment
            equipment_type, equipment = self.equipment_list[serial_port]

            # Delete the selected equipment
            if equipment_type == 'Syringe group':

                # Process all syringes
                for syringe_axis in equipment.syringe_equipments.keys():
                    if equipment.syringe_equipments[syringe_axis] is not None:

                        # Get the widget
                        widget = equipment.syringe_equipments[syringe_axis].widget

                        # Remove the syringe
                        self.parent.groupDisplay.deleteSyringe(widget)

            elif equipment_type == 'Flowmeter':
                self.parent.groupDisplay.deleteFlowMeter(equipment.widget)

            # Reload the table
            self.fillEquipmentTable()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------------
    # Modify the selected equipment
    def editEquipment(self, serial_port=None):

        # Get the equipment
        equipment_type, equipment = self.equipment_list[serial_port]

        # Call the appropriate edit window
        if equipment_type == 'Syringe group':
            openWindow(self.parent, setArduinoGroupWindow, 'arduino_group', arduino_class=equipment)

        elif equipment_type == 'Flowmeter':
            openWindow(self.parent, setFlowMeterWindow, 'flow_meter', flowmeter=equipment)
