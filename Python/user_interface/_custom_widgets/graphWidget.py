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

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

# ---------------------------
# Widget for matplotlib graph
class SingleGraph (FigureCanvasQTAgg):

    """ Script taken from https://www.mfitzp.com/tutorials/plotting-matplotlib/ """

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        super(SingleGraph, self).__init__(fig)

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE GRAPH
    ##-/-/-/-/-/-/-/-/

    # -------------------------------
    # Set the name of the axis labels
    def setLabels(self, label_names=['X','Y']):
        self.axes.set_xlabel(label_names[0])
        self.axes.set_ylabel(label_names[1])
