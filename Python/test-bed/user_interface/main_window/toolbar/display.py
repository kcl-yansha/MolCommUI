import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.path_to_assets import getIcon

from user_interface.main_window.toolbar.functions import toolBarFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## TOOLBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/

class toolBar (toolBarFunctions):
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent

        # Make the toolbar
        self.actionTools = self.parent.addToolBar("Actions")

        # Populate the toolbar
        self.createActionToolbar()

        # Apply settings to the toolbar
        self.actionTools.setMovable(False)

    # --------------------
    # Populate the toolbar
    def createActionToolbar(self):

        # Add the button to connect
        self.connectTool = qtw.QAction( getIcon('connect_button.png'), 'Connect to...', self.parent)
        self.connectTool.triggered.connect(self.callEquipmentConnectionWindow)
        self.connectTool.setToolTip("Start connection to an equipment.")
        self.actionTools.addAction( self.connectTool )

        # Add the button to add a new group
        self.newGroupTool = qtw.QAction( getIcon('new_button.png'), 'New group...', self.parent)
        #self.newGroupTool.triggered.connect(self.callEquipmentConnectionWindow)
        self.newGroupTool.setToolTip("Add a new group of equipment.")
        self.actionTools.addAction( self.newGroupTool )

        # Add the button to load settings
        self.settingTool = qtw.QAction( getIcon('open_button.png'), 'Load settings...', self.parent)
        self.settingTool.setToolTip("Load a setting file.")
        self.actionTools.addAction( self.settingTool )
