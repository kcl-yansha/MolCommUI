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

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface.dock_window.scheduler_controller.display import SchedulerControllerPanel
from user_interface.dock_window.spectrum_window.display import SpectrumDisplayPanel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarWindowFunctions(object):

    ##-\-\-\-\-\-\
    ## Window MENU
    ##-/-/-/-/-/-/

    # ---------------------------
    # Open the graph display dock
    def callSchedulerControllerDock(self):

        # Open the dock
        _open_dock = True
        if "graph" in self.parent.docks.keys():
            if self.parent.docks["scheduler"] is not None:
                _open_dock = False

        if _open_dock:
            self.parent.docks["scheduler"] = SchedulerControllerPanel("Scheduler", self.parent)
            self.parent.addDockWidget(qtc.Qt.BottomDockWidgetArea, self.parent.docks["scheduler"])

            # Set the size and attach the dock
            self.parent.docks["scheduler"].setFloating(True)
            #self.parent.docks["scheduler"].detectLocationChange()
            #self.parent.docks["scheduler"].setFloating(False)

    # ------------------------------
    # Open the spectrum display dock
    def callSpectrumDisplayDock(self):

        # Open the dock
        _open_dock = True
        if "spectrum" in self.parent.docks.keys():
            if self.parent.docks["spectrum"] is not None:
                _open_dock = False

        if _open_dock:
            self.parent.docks["spectrum"] = SpectrumDisplayPanel("Spectrum Display", self.parent)
            self.parent.addDockWidget(qtc.Qt.RightDockWidgetArea, self.parent.docks["spectrum"])

            # Set the size and attach the dock
            self.parent.docks["spectrum"].setFloating(True)
            #self.parent.docks["spectrum"].detectLocationChange()
            #self.parent.docks["spectrum"].setFloating(False)
