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

import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface.groups.syringe_items.display import SyringeGroup
from user_interface.groups.flowmeter_items.display import FlowMeterGroup
from user_interface.groups.spectrometer_items.display import SpectroMeterGroup

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class EquipmentGroupsFunctions(object):

    ##-\-\-\-\-\-\-\
    ## UPDATE THE UI
    ##-/-/-/-/-/-/-/

    # ------------------------
    # Regenerate the interface
    def refreshUI(self):

        # Get the informations
        new_elements = [[self._get_widget_type(x), y] for x, y in self.groups]

        # Delete all groups
        for i in reversed( range(self.layout.count()) ):
            self.layout.itemAt(i).widget().deleteLater()
        self.groups = []

        # Populate all groups
        for wgenerator, object in new_elements:
            wgenerator(object)

    ##-\-\-\-\-\-\-\-\
    ## ACCESS ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # -----------------------------
    # Return the list of all groups
    def listGroupInstances(self):

        # Initialise the list
        all_equipment = []

        for widget, instance in self.groups:

            # Accept syringes
            if isinstance(widget, SyringeGroup):
                all_equipment.append(instance.equipment)

            else:
                all_equipment.append(instance)

        return all_equipment

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ----------------------------
    # Add a syringe to the display
    def addSyringe(self, syringe):

        # Prepare the widget
        crt_widget = SyringeGroup(self.parent, syringe=syringe)

        # Add it to the system
        self.groups.append([crt_widget, syringe])
        self.layout.addWidget( crt_widget )

    # -----------------------
    # Delete the syringe item
    def deleteSyringe(self, widget):

        # Disconnect the syringe pump
        self.parent.equipments['syringe_pumps'].remove(widget.syringe)
        remove_all = widget.syringe.removeSyringe()

        # Remove port if empty
        if remove_all:
            self.parent.active_ports.remove(widget.syringe.syringe_group.serial_port)

        # Search for the group to remove
        all_widget = [x for x, y in self.groups]
        w_id = all_widget.index(widget)

        # Remove the group
        self.groups.pop(w_id)

        # Refresh the UI
        self.refreshUI()

    # ------------------------------
    # Add a flowmeter to the display
    def addFlowMeter(self, flowmeter):

        if flowmeter.assigned_pump is None:

            # Prepare the widget
            crt_widget = FlowMeterGroup(self.parent, flowmeter=flowmeter)

            # Add it to the system
            self.groups.append([crt_widget, flowmeter])
            self.layout.addWidget( crt_widget )

    # -------------------------
    # Delete the flowmeter item
    def deleteFlowMeter(self, widget):

        # Disconnect the flowmeter
        self.parent.equipments['flow_meter'].remove(widget.flowmeter)
        self.parent.active_ports.remove(widget.flowmeter.serial_port)

        # Close the connection
        widget.flowmeter.close()

        # Search for the group to remove
        all_widget = [x for x, y in self.groups]
        w_id = all_widget.index(widget)

        # Remove the group
        self.groups.pop(w_id)

        # Refresh the UI
        self.refreshUI()

    # ---------------------------------
    # Add a spectrometer to the display
    def addSpectroMeter(self, spectrometer):

        # Prepare the widget
        crt_widget = SpectroMeterGroup(self.parent, spectrometer=spectrometer)

        # Add it to the system
        self.groups.append([crt_widget, spectrometer])
        self.layout.addWidget( crt_widget )

    # ----------------------------
    # Delete the spectrometer item
    def deleteSpectroMeter(self, widget):

        # Disconnect the flowmeter
        self.parent.equipments['spectrometer'].remove(widget.spectrometer)
        self.parent.active_ports.remove(widget.spectrometer.serial_number)

        # Close the connection
        widget.spectrometer.close()

        # Search for the group to remove
        all_widget = [x for x, y in self.groups]
        w_id = all_widget.index(widget)

        # Remove the group
        self.groups.pop(w_id)

        # Refresh the UI
        self.refreshUI()

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## DEFINE THE DRAG & DROP ACTION
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------
    # Accept drag events
    def dragEnterEvent(self, event):
        self.dragged = self.content.mapFrom( self,  event.pos() ).y()

        if len(self.groups) > 1:
            event.accept()

    # --------------------
    # React on drop events
    def dropEvent(self, event):

        # Grab the position
        position = self.content.mapFrom( self,  event.pos() ).y()

        if len(self.groups) > 1:
            # Find the new group location
            self.getBordingGroups(position)

            # Accept the event
            event.accept()

    # ------------------------------------
    # Get the groups bording the positions
    def getBordingGroups(self, pos_y):

        # Get all the widgets positions and height
        group_positions = np.array( [x.y() for x, y in self.groups])

        # Calculate the two closest group
        group_height = np.array( [x.height() for x, y in self.groups])
        group_mid_positions = group_positions + group_height/2

        diff_positions_origin = np.abs( group_mid_positions - self.dragged )
        diff_positions_new = np.abs( group_mid_positions - pos_y )

        # Get the closest groups
        groupOrigin = np.argmin( diff_positions_origin )
        groupA, groupB = np.argsort( diff_positions_new )[:2]

        # Move the group
        self.moveGroupTo(groupOrigin, np.amin([groupA, groupB]))

    ##-\-\-\-\-\-\-\-\-\
    ## RE-ARRANGE GROUPS
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Get the type of widget for regeneration
    def _get_widget_type(self, object):

        # Check if its a syringe group
        if isinstance(object, SyringeGroup):
            new_widget = self.addSyringe

        # Check if its a flowmeter
        elif isinstance(object, FlowMeterGroup):
            new_widget = self.addFlowMeter

        # Check if its a spectrometer
        elif isinstance(object, SpectroMeterGroup):
            new_widget = self.addSpectroMeter

        # Set as none
        else:
            new_widget = None

        return new_widget

    # -------------------------------------------
    # Move the selected group to the new position
    def moveGroupTo(self, old_ID, new_ID):

        # Coerce the IDs
        if old_ID > new_ID:
            new_ID += 1

        # Move the index
        self.groups.insert( new_ID, self.groups.pop(old_ID) )

        # Refresh the UI
        self.refreshUI()

    # ------------------------------------------------------
    # Move the selected group inside a synchronisation group
    def moveGroupInside(self, old_ID, new_ID):

        # Get the widgets
        sync_group, _ = self.groups[new_ID]
        _, equipment = self.groups[old_ID]

        # Add the widget to the sync group
        sync_group.addToGroup(equipment)

        # Remove the old group from the list
        self.groups.pop(old_ID)

        # Refresh the UI
        self.refreshUI()
