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

##-\-\-\-\-\-\-\-\-\-\-\-\
## LABEL WITH SPECIFIC TEXT
##-/-/-/-/-/-/-/-/-/-/-/-/

# ---------------------
# Generate a bold label
class CTableWidget(qtw.QTableWidget):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QTableWidget.__init__(self, *args, **kwargs)

        # Set the parameters
        self.n_cols = 1

    ##-\-\-\-\-\
    ## EDIT TABLE
    ##-/-/-/-/-/

    # ----------------------------
    # Set the labels for the table
    def setLabels(self, header_list):

        # Get the number of columns
        self.n_cols = len(header_list)

        # Set the labels
        self.setHorizontalHeaderLabels(header_list)

    # ----------------------
    # Reinitialise the table
    def reset(self):

        rowCount = self.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.removeRow(0)

    # ------------------
    # Resize the columns
    def resizeCols(self):

        header = self.horizontalHeader()
        for i in range( self.n_cols ):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)
