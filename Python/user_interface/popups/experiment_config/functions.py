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

from input_output.misc import date2str
from input_output.experiments.experiment_class import setExperiment

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setExperimentFunctions(object):

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------------------------
    # Browse for the default folder to use
    def browsePath(self):

        # Browse for the file setting
        defaultFolder = qtw.QFileDialog.getExistingDirectory(self.parent, "Select Default Folder", self.parent.current_folder, qtw.QFileDialog.ShowDirsOnly)

        # Process
        if defaultFolder != "":

            # Update the last selected folder
            self.parent.current_folder = defaultFolder

            # Apply the change
            self.folderBrowsing.setText(defaultFolder)

    # ---------------------
    # Apply all the changes
    def saveExperimentDetails(self):

        # Collect the information
        name = self.nameEntry.text()
        path = self.folderBrowsing.text()
        comments = self.commentEntry.toPlainText()

        # Get the date from the widget
        date_object = self.dateEntry.dateTime()
        date_text = date2str(date_object)

        # Generate the experiment
        new_experiment = setExperiment(self.parent, name=name, date_and_time=date_text, folder=path, comments=comments)

        # Save the experiment in the parent
        self.parent.experiment = new_experiment
        self.parent.experimentDisplay.setExperimentName(new_experiment.name)
        self.parent.experimentDisplay.setExperimentStatus(new_experiment.recording)

        # Close the windows
        self.close()
