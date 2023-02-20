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

from functools import partial
import pyqtgraph as pg

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._custom_widgets.customLabel import BoldLabel

from plotting.spectrum_plot import SpectrumPlot

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class SpectrumDisplayFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # --------------------------------
    # Update the display of the graphs
    def displayGraphs(self):

        # Reset the display
        for i in reversed(range(self.graphDisplayLayout.count())):
            self.graphDisplayLayout.itemAt(i).widget().setParent(None)

        self.graphs = {}

        # Add the intensity graph window
        self.graphWidget = pg.GraphicsLayoutWidget()
        self.graphWidget.setBackground('#1F272B')

        # Intensity
        self.graphPlot = self.graphWidget.addPlot()
        self.graphPlot.setLabel('bottom', 'Wavelength [nm]')
        self.graphPlot.setLabel('left', 'Intensity [AU]')
        self.graphPlot.setYRange(0, 65535, padding=0)

        self.graphDisplayLayout.addWidget( self.graphWidget )

        # Add the lines
        self.refreshLines()

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE MAIN GRAPH
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Refresh the displayed spectrum
    def refreshSpectrum(self, spectrometer):

        # Extract values from the instance
        wavelength = spectrometer.wavelengths
        graph_id = spectrometer.file_name

        # Initialise the scale if missing
        if len( self.graphs.keys() ) == 0:
            self.graphPlot.setXRange(wavelength[0], wavelength[-1], padding=0)
            self.absorbancePlot.setXRange(wavelength[0], wavelength[-1], padding=0)

        # Initialise the graph if missing
        if graph_id not in self.graphs.keys():
            self.graphs[graph_id] = SpectrumPlot(spectrometer)

        # Update the values
        self.graphs[graph_id].updateSpectrum()

        # Update the graphs
        self.updateIntensity(graph_id)
        self.updateAbsorbance(graph_id)

    # --------------------------
    # Update the intensity graph
    def updateIntensity(self, graph_id):

        # Initialise the graph if missing
        if self.graphs[graph_id].i_plot is None:

            # Add the new plot
            self.graphs[graph_id].i_plot = self.graphPlot.plot( pen=pg.mkPen('#ffffff', width=2) )

            # Draw the limit
            self.plotArea(self.graphs[graph_id].spectrometer.wavelengths)

            # Draw the baseline
            if self.graphs[graph_id].spectrometer.baseline is not None:
                self.refreshBaseline(self.graphs[graph_id])

        # Update the graph
        self.graphs[graph_id].setIntensity()

    # ---------------------------
    # Update the absorbance graph
    def updateAbsorbance(self, graph_id):

        if self.absorbancePlot is not None and self.graphs[graph_id].spectrometer.baseline is not None:

            # Initialise the graph if missing
            if self.graphs[graph_id].a_plot is None:

                # Add the new plot
                self.graphs[graph_id].a_plot = self.absorbancePlot.plot( pen=pg.mkPen('#ffffff', width=2) )

            # Update the graph
            self.graphs[graph_id].setAbsorbance()

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## UPDATE ADDITIONAL GRAPH
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Refresh the displayed baseline
    def refreshBaseline(self, graph):

        # Get the info
        graph_id = graph.spectrometer.file_name + '_baseline'

        # Initialise the graph if missing
        if graph_id not in self.graphs.keys():

            # Add the new plot
            self.graphs[graph_id] = self.graphPlot.plot(
            pen=pg.mkPen('#ffff00', width=1)
            )

        # Update the graph
        self.graphs[graph_id].setData(graph.spectrometer.wavelengths, graph.spectrometer.baseline)

    # ----------------------------------------------------
    # Display the line at which the intensity are rescaled
    def refreshScaleLine(self):

        # Retrieve the value from the display
        wavelength = self.referenceSelection.value()

        # Update the graphs
        for spectrometer in self.graphs.values():
            if isinstance(spectrometer, SpectrumPlot):
                spectrometer.spectrometer.w_rescale = wavelength

        if True:

            # Initialise the graph if missing
            if 'scale_line' not in self.graphs.keys():
                self.graphs['scale_line'] = self.graphPlot.plot(
                pen=pg.mkPen('#ffff00', width=1, style=qtc.Qt.DashLine)
                )

            # Update the graph
            self.graphs['scale_line'].setData([wavelength, wavelength],[0,65535])

        else:
            pass

    # -----------------
    # Display all lines
    def refreshLines(self):
        self.refreshScaleLine()

    # ----------------------------
    # Reload the style of the line
    def _refreshLineStyle(self, graph_id): # TO BE REMOVED

        # Clean the UI
        self.graphs[graph].plot.clear()

        # Replace the graph
        drawplot = self.graphPlot.plot( pen=pg.mkPen(self.graphs[graph].color, width=self.graphs[graph].width) )

        # Update the UI
        self.graphs[graph].plot = drawplot

    # -----------------------
    # Plot the intensity area
    def plotArea(self, wavelength, i_optimum=50000, i_range=10000):

        # Compute the limits
        i_low = i_optimum - i_range
        i_high = i_optimum + i_range

        # Prepare the brushes
        brush = pg.mkBrush((255,0,0,50), alpha=0.25)
        pen = pg.mkPen('#ff0000', width=1, style=qtc.Qt.DashLine)

        # Generate the items to plot
        phigh = pg.PlotCurveItem([wavelength[0],wavelength[-1]], [i_low,i_low])
        plow = pg.PlotCurveItem([wavelength[0],wavelength[-1]], [i_high,i_high])
        poptimal = pg.PlotCurveItem([wavelength[0],wavelength[-1]], [i_optimum,i_optimum], pen = pen)

        pfill = pg.FillBetweenItem(phigh, plow, brush = brush)

        # Plot the items
        self.graphPlot.addItem(poptimal)
        self.graphPlot.addItem(pfill)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -----------------
    # Adapt the display
    def switchDisplay(self):

        # Make a copy of the dictionary
        crt_graph = self.graphs.copy()

        # Remove graph that needs to be redone
        for graph in crt_graph.keys():
            if not isinstance(crt_graph[graph], SpectrumPlot):
                self.graphs.pop(graph)

        # Refresh the graph
        self.displayGraphs()

    # ----------------
    # Get the baseline
    def setBaseline(self):

        # Make a copy of the dictionary
        crt_graph = self.graphs.copy()

        # Process all connected spectrometers
        for spectrometer in crt_graph.values():
            if isinstance(spectrometer, SpectrumPlot):

                # Set the baseline
                spectrometer.setBaseline()

                # Plot the baseline
                self.refreshBaseline(spectrometer)
