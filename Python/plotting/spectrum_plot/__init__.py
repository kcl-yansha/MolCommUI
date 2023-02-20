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

import numpy as np

class SpectrumPlot:
    def __init__(self, spectrometer):

        # Connect to other instances
        self.spectrometer = spectrometer

        self.i_plot = None
        self.a_plot = None

    ##-\-\-\-\-\-\-\-\
    ## DATA MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # -------------------
    # Update the spectrum
    def updateSpectrum(self):
        self.spectrometer.updateSpectrum()

    # -----------------------------
    # Set the baseline of the graph
    def setBaseline(self):
        self.spectrometer.setBaseline()

    ##-\-\-\-\-\-\
    ## GRAPH UPDATE
    ##-/-/-/-/-/-/

    # ----------------------------
    # Update the intensity display
    def setIntensity(self):

        if self.i_plot is not None:
            self.i_plot.setData(self.spectrometer.wavelengths, self.spectrometer.last_values)

    # -----------------------------
    # Update the absorbance display
    def setAbsorbance(self):

        if self.a_plot is not None:
            self.a_plot.setData(self.spectrometer.wavelengths, self.spectrometer.absorption)
