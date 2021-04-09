import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._style.color_theme import applyStyle

from user_interface.main_window.menubar.display import menuBar
from user_interface.main_window.toolbar.display import toolBar
from user_interface.groups.group_interface.display import EquipmentGroups

##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUI(qtw.QMainWindow):
    def __init__(self, application):
        super(mainGUI, self).__init__()

        # Initialize the properties of the software Main GUI
        self.application = application
        self.title = "Test"
        self.version = "alpha"

        # Initialize the sub-windows and docks containers
        self.subWindows = {}
        self.docks = {
        'terminal': None
        }

        # Initialize the list of equipment
        self.equipments = {}

        # Generate the display
        self.setWindowTitle(self.title + " (" + self.version + ")")

        # Apply the style
        applyStyle( self.application )

        # Generate the central widget
        self.createCentralWidget()

        # Add the status bar to the window
        self.statusBar = qtw.QStatusBar()
        self.setStatusBar(self.statusBar)

        # Add the menu and toolbars
        self.menuBar = menuBar(self)
        self.toolBar = toolBar(self)

        # Display the window
        self.show()
        self.setMinimumSize(575,725)

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## DISPLAY THE MAIN WINDOW
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Create the central widget of the window
    def createCentralWidget(self):

        # Define the widget
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Display the group display
        self.groupDisplay = EquipmentGroups(self)
        self.mainLayout.addWidget(self.groupDisplay)

        # Display the widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
