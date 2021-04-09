import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface.main_window.menubar.functions_equipment import menuBarEquipmentFunctions
from user_interface.main_window.menubar.functions_window import menuBarWindowFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## MENUBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/

class menuBar (menuBarEquipmentFunctions, menuBarWindowFunctions):
    def __init__(self, parent):

        # Initialise the menu bar
        self.parent = parent
        self.mainMenu = self.parent.menuBar()
        self.mainMenu.setNativeMenuBar(False)

        # Call the different submenus
        self.createFileMenu()
        self.createEquipmentMenu()
        self.createWindowMenu()

    ##-\-\-\-\-\-\-\-\-\-\
    ## INTERFACE GENERATION
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------
    # Generate the FILE submenu
    def createFileMenu(self):

        # Initialise
        self.fileMenu = self.mainMenu.addMenu("File")
        self.fileMenu.setToolTipsVisible(True)

        #self.equipmentMenu.addSeparator()

        # Open particle detection window
        self.fileMenu.quitButton = qtw.QAction("Quit", self.parent)
        self.fileMenu.quitButton.setShortcut("Ctrl+Q")
        self.fileMenu.quitButton.setToolTip("Close the software.")
        self.fileMenu.quitButton.triggered.connect(self.parent.close)
        self.fileMenu.addAction(self.fileMenu.quitButton)

    # ------------------------------
    # Generate the EQUIPMENT submenu
    def createEquipmentMenu(self):

        # Initialise
        self.equipmentMenu = self.mainMenu.addMenu("Equipment")
        self.equipmentMenu.setToolTipsVisible(True)

        # Save image menu
        self.equipmentMenu.connectToSubmenu = qtw.QMenu('Connect to...', self.parent)
        self.equipmentMenu.connectToSubmenu.setToolTipsVisible(True)

        # Single frame
        self.equipmentMenu.syringePump = qtw.QAction("Syringe Pump", self.parent)
        self.equipmentMenu.syringePump.setToolTip("Connect to a syringe pump.")
        self.equipmentMenu.syringePump.triggered.connect(self.callSyringeGroupWindow)
        self.equipmentMenu.connectToSubmenu.addAction(self.equipmentMenu.syringePump)

        self.equipmentMenu.addMenu(self.equipmentMenu.connectToSubmenu)

        #self.equipmentMenu.addSeparator()

    # ---------------------------
    # Generate the WINDOW submenu
    def createWindowMenu(self):

        # Initialise
        self.windowMenu = self.mainMenu.addMenu("Window")
        self.windowMenu.setToolTipsVisible(True)

        # Open particle detection window
        self.windowMenu.terminalViewButton = qtw.QAction("Terminal Output", self.parent)
        self.windowMenu.terminalViewButton.setShortcut("Ctrl+Shift+T")
        self.windowMenu.terminalViewButton.setToolTip("Display the output of the terminal.")
        self.windowMenu.terminalViewButton.triggered.connect(self.callTerminalOutputDock)
        self.windowMenu.addAction(self.windowMenu.terminalViewButton)

        #self.windowMenu.addSeparator()
