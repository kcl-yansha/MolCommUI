import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._custom_widgets.scrollLabel import ScrollLabel
from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.terminal_output.functions import TerminalOutputFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class TerminalOutputPanel(qtw.QDockWidget, TerminalOutputFunctions):
    def __init__(self, name, parent):
        super(TerminalOutputPanel, self).__init__(name, parent)

        # Initialise the subwindow
        self.parent = parent
        self.setAllowedAreas( qtc.Qt.LeftDockWidgetArea | qtc.Qt.RightDockWidgetArea )

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Populate the panel
        self.createTextDisplay(self.mainLayout)
        self.mainLayout.addWidget( HorizontalSeparator() )
        self.createButtonDisplay(self.mainLayout)

        # Start the redirection of the terminal output
        self.catchTerminal()

        # Display the panel
        self.mainLayout.setAlignment(qtc.Qt.AlignTop)
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        #self.show()
        self.setMinimumSize(550,650)

        # Add listeners
        #self.topLevelChanged.connect(self.detectLocationChange)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Release the terminal redirection
        sys.stdout = sys.__stdout__

        # Close the window
        event.accept()

        # Disconnect the dock from the software
        self.parent.removeDockWidget(self.parent.docks["terminal"])
        self.parent.docks["terminal"] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Generate the widget to select a path
    def createTextDisplay(self, parentWidget):

        self.terminalOutputWidget = qtw.QWidget()
        self.terminalOutputLayout = qtw.QVBoxLayout(self.terminalOutputWidget)

        # Add the scrollabel text label
        self.terminalOutputLabel = ScrollLabel()
        self.terminalOutputLayout.addWidget(self.terminalOutputLabel)

        # Set the style of the scroll label
        self.terminalOutputLabel.label.setStyleSheet("background-color: black; color: yellow")

        self.terminalOutputWidget.setLayout(self.terminalOutputLayout)
        parentWidget.addWidget(self.terminalOutputWidget)

    # -----------------------------------------
    # Generate the widget with the user actions
    def createButtonDisplay(self, parentWidget):

        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QVBoxLayout(self.buttonWidget)

        clearButton = qtw.QPushButton('Clear')
        clearButton.released.connect(self.terminalOutputLabel.clearText)
        self.buttonLayout.addWidget(clearButton)

        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)
