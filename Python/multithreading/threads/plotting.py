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

import sys
import pyqtgraph as pg
import time
import traceback


import PyQt5.QtCore as qtc

from plotting.time_plot import TimePlot

##-\-\-\-\-\-\
## SIGNAL CLASS
##-/-/-/-/-/-/

class WorkerSignals(qtc.QObject):

    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    result = qtc.pyqtSignal(float)
    progress = qtc.pyqtSignal(int)

##-\-\-\-\-\-\-\-\-\-\
## MAIN PROCESS THREAD
##-/-/-/-/-/-/-/-/-/-/

class PlottingThread(qtc.QThread):

    def __init__(self, graphWindow): #, fn, *args, **kwargs):
        parent = None
        super(PlottingThread, self).__init__(parent)

        # Link to the graph
        self.graphWindow = graphWindow

        # Define the constant
        self.runs = True

        # Define the parameters
        self.max_points = 100

        # Assign the signals
        self.signals = WorkerSignals()

    ##-\-\-\-\-\-\
    ## MAIN THREAD
    ##-/-/-/-/-/-/

    # --------------
    # Run the thread
    def run(self):

        while self.runs:

            # Plot all the graphs
            for graph in self.graphWindow.graphs.keys():

                # Get the values
                x, y = self.graphWindow.graphs[graph].time, self.graphWindow.graphs[graph].y

                # Plot them
                self.graphWindow.graphs[graph].plot.setData(x, y)

            # Wait until next loop
            qtc.QThread.msleep(100)

    ##-\-\-\-\-\-\-\
    ## MANAGE VALUES
    ##-/-/-/-/-/-/-/

    # ------------------------
    # Add a value to the graph
    def addValue(self, graph, values):

        # Initialise the graph if needed
        if graph not in self.graphWindow.graphs.keys():

            drawplot = self.graphWindow.graphPlot.plot()
            self.graphWindow.graphs[graph] = TimePlot(graph, drawplot)

            # Add the controls to the window
            self.graphWindow.addGraph(graph)

        # Add the value to the graph
        self.graphWindow.graphs[graph].addValue(values, self.max_points)

    # ---------------------------------
    # Clear all the values in the graph
    def clearValue(self):

        # Process all the values
        for graph in self.graphWindow.graphs.keys():
            self.graphWindow.graphs[graph].clearValue()

    ##-\-\-\-\-\-\
    ## MANAGE STYLE
    ##-/-/-/-/-/-/

    # -----------------------------
    # Change the style of the graph
    def changePlotStyle(self, graph):

        # Replace the graph
        drawplot = self.graphWindow.graphPlot.plot( pen=pg.mkPen(self.graphWindow.graphs[graph].color, width=self.graphWindow.graphs[graph].width) )

        # Update the UI
        self.graphWindow.graphs[graph].plot.clear()
        self.graphWindow.graphs[graph].plot = drawplot

    ##-\-\-\
    ## OTHERS
    ##-/-/-/

    # ---------------------
    # Interrupt the process
    def stop(self):
        self.runs = False
