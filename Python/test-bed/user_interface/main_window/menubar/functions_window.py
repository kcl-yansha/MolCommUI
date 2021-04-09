import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface.terminal_output.display import TerminalOutputPanel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarWindowFunctions(object):

    ##-\-\-\-\-\-\
    ## Window MENU
    ##-/-/-/-/-/-/

    # -----------------------------
    # Open the terminal output dock
    def callTerminalOutputDock(self):

        # Open the dock
        _open_dock = True
        if "terminal" in self.parent.docks.keys():
            if self.parent.docks["terminal"] is not None:
                _open_dock = False

        if _open_dock:
            self.parent.docks["terminal"] = TerminalOutputPanel("Terminal Output", self.parent)
            self.parent.addDockWidget(qtc.Qt.RightDockWidgetArea, self.parent.docks["terminal"])

            # Set the size and attach the dock
            self.parent.docks["terminal"].setFloating(True)
            #self.parent.docks["terminal"].detectLocationChange()
            #self.parent.docks["terminal"].setFloating(False)
