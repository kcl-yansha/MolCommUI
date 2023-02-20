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

import pyqtgraph as pg
import time

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.dock_window.spectrum_window.functions import SpectrumDisplayFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class SpectrumDisplayPanel(qtw.QDockWidget, SpectrumDisplayFunctions):
    def __init__(self, name, parent):
        super(SpectrumDisplayPanel, self).__init__(name, parent)

        # Set the parameters
        self.graphs = {}
        self.absorbance = {}
        self.init_time = time.time()

        # Initialise the subwindow
        self.parent = parent
        self.graph_widgets = {}
        self.color_button = {}
        self.width_button = {}
        self.setAllowedAreas( qtc.Qt.LeftDockWidgetArea | qtc.Qt.RightDockWidgetArea )

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Populate the panel
        self.createSpectrumDisplay(self.mainLayout)
        self.mainLayout.addWidget( HorizontalSeparator() )
        self.createCommandDisplay(self.mainLayout)

        # Initialise the display
        self.displayGraphs()

        # Display the panel
        self.mainLayout.setAlignment(qtc.Qt.AlignTop)
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        #self.show()
        #self.setMinimumSize(550,650)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()

        # Disconnect the dock from the software
        self.parent.removeDockWidget(self.parent.docks["spectrum"])
        self.parent.docks["spectrum"] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Generate the widget to select a path
    def createSpectrumDisplay(self, parentWidget):

        # Generate the widget
        self.graphDisplayWidget = qtw.QWidget()
        self.graphDisplayLayout = qtw.QVBoxLayout(self.graphDisplayWidget)

        # Display the widget
        self.graphDisplayWidget.setLayout(self.graphDisplayLayout)
        parentWidget.addWidget(self.graphDisplayWidget)

    # -----------------------------------------
    # Generate the widget with the user actions
    def createCommandDisplay(self, parentWidget):

        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QGridLayout(self.buttonWidget)

        currentRow = 0

        # Baseline
        self.baselineButton = qtw.QPushButton('Set Baseline')
        self.baselineButton.released.connect(self.setBaseline)
        self.buttonLayout.addWidget(self.baselineButton, currentRow, 0, 1, 2)

        currentRow += 1

        # Rescaling ref
        self.buttonLayout.addWidget(qtw.QLabel('Reference (nm):'), currentRow, 0)

        self.referenceSelection = qtw.QDoubleSpinBox()
        self.referenceSelection.setDecimals(2)
        self.referenceSelection.setMinimum(200)
        self.referenceSelection.setMaximum(1000)
        self.referenceSelection.setValue(500)
        self.referenceSelection.valueChanged.connect(self.refreshScaleLine)
        self.buttonLayout.addWidget(self.referenceSelection, currentRow, 1)

        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)
