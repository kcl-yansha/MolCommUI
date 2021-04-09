import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class EquipmentGroupsFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## DEFINE THE DRAG & DROP ACTION
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------
    # Accept drag events
    def dragEnterEvent(self, event):
        self.dragged = self.content.mapFrom( self,  event.pos() ).y()
        event.accept()

    # --------------------
    # React on drop events
    def dropEvent(self, event):

        # Grab the position
        position = self.content.mapFrom( self,  event.pos() ).y()

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

        # Check if entering a sync group
        is_ingroup, sync_group = self.checkSyncGroup(groupOrigin, groupA, groupB, pos_y)

        # Move the group
        if is_ingroup:
            self.moveGroupInside(groupOrigin, sync_group)
        else:
            self.moveGroupTo(groupOrigin, np.amin([groupA, groupB]))

    # -------------------------
    # Get if synchronised group
    def checkSyncGroup(self, grpO, grpA, grpB, position):

        # Check that the dragged group is not a sync group
        if self.groups[grpO][1] == 'sync_group':
            return False, None

        # Check if entering a sync group
        else:
            if self.groups[grpA][1] == 'sync_group' or self.groups[grpB][1] == 'sync_group':

                # Check which object is a sync group
                if self.groups[grpA][1] == 'sync_group':
                    sync_group = grpA
                else:
                    sync_group = grpB

                # Get all the sync group min and max position
                group_min = np.array( [x.y() for x, y in self.groups])[sync_group]
                group_max = group_min + np.array( [x.height() for x, y in self.groups])[sync_group]

                # Check if the new object is in range
                if position >= group_min and position <= group_max:
                    return True, sync_group
                else:
                    return False, None

            else:
                return False, None

    ##-\-\-\-\-\-\-\-\-\
    ## RE-ARRANGE GROUPS
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------------
    # Move the selected group to the new position
    def moveGroupTo(self, old_ID, new_ID):

        # Coerce the IDs
        if old_ID > new_ID:
            new_ID += 1

        # Move the index
        self.groups.insert( new_ID, self.groups.pop(old_ID) )

        # Get the informations
        new_elements = [[x.title(), y] for x, y in self.groups]

        # Delete all groups
        for i in reversed( range(self.layout.count()) ):
            self.layout.itemAt(i).widget().deleteLater()
        self.groups = []

        # Populate all groups
        from user_interface.groups.sync_group.display import SynchronisedGroup
        from user_interface.groups.syringe_items.display import SyringeGroup

        for title, etype in new_elements:

            if etype == 'syringe_pump':
                crt_widget = SyringeGroup(self.parent, title=title)
            else:
                crt_widget = SynchronisedGroup(self.parent, title=title)

            self.layout.addWidget( crt_widget )
            self.groups.append([crt_widget, etype])

    # ------------------------------------------------------
    # Move the selected group inside a synchronisation group
    def moveGroupInside(self, old_ID, new_ID):

        # Get the widgets
        sync_group, _ = self.groups[new_ID]
        moved_group, _ = self.groups[old_ID]

        # Add the widget to the sync group
        sync_group.addNewGroup(moved_group)

        # Remove the old group from the list
        self.groups.pop(old_ID)

        # Get the informations
        new_elements = [[x.title(), y] for x, y in self.groups]

        # Delete all groups
        for i in reversed( range(self.layout.count()) ):
            self.layout.itemAt(i).widget().deleteLater()
        self.groups = []

        # Populate all groups
        from user_interface.groups.sync_group.display import SynchronisedGroup
        from user_interface.groups.syringe_items.display import SyringeGroup

        for title, etype in new_elements:

            if etype == 'syringe_pump':
                crt_widget = SyringeGroup(self.parent, title=title)
            else:
                crt_widget = SynchronisedGroup(self.parent, title=title)

            self.layout.addWidget( crt_widget )
            self.groups.append([crt_widget, etype])
