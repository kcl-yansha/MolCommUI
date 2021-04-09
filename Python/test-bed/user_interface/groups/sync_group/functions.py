import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class SynchronisedGroupFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## GENERATE CONTEXT MENU
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Display the menu on a right click
    def showRightClickMenu(self, event):

        # Initialise the menu
        self.menu = qtw.QMenu()

        # Rename the group
        rename_action = self.menu.addAction("Rename group")
        rename_action.triggered.connect(self.renameGroup)

        # Display the menu at the mouse location
        action = self.menu.exec_(self.mapToGlobal(event))

    # ----------------
    # Rename the group
    def renameGroup(self):

        # Prompt the user
        new_name, ok = qtw.QInputDialog.getText(self.parent, 'Group Name', 'Enter the new name for the group', qtw.QLineEdit.Normal, self.title())

        # Modify if required
        if ok:
            self.setTitle(new_name)

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## ADD WIDGET TO THE GROUP
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Add a new group to synchronise
    def addNewGroup(self, object):

        # Empty first if needed
        if self.empty:
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().deleteLater()
        self.empty = False

        # Add the widget
        self.layout.addWidget( object )
