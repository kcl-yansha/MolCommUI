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

from datetime import datetime
import numpy as np
import os
import time

from input_output.folder_management import checkPreviousFolder
from input_output.misc import date2str
from input_output.experiments.files import write2file

##-\-\-\-\-\-\-\-\
## EXPERIMENT CLASS
##-/-/-/-/-/-/-/-/

class Experiment:
    def __init__(self, parent, name, date_and_time, folder, comments):

        # Assign the parent
        self.parent = parent

        # Set the experiment parameters
        self.name = name
        self.date_and_time = date_and_time
        self.folder = folder
        self.comments = comments

        # Set the initial time
        self.init_time = time.time()
        self.recording = False

    ##-\-\-\-\-\-\-\
    ## WRITE IN FILE
    ##-/-/-/-/-/-/-/

    # -----------------------
    # Write the value in file
    def save(self, path, value, header=None, delimiter=','):

        if self.recording:

            # Build the path
            file_path = os.path.join(self.folder, self.name.lower().replace(' ','_') + '_' + path + '.csv')

            # Get the time
            crt_time = time.time() - self.init_time

            # Add the time to the value
            if isinstance(value, np.ndarray):
                array = np.insert(value, 0, crt_time)
            else:
                array = np.array([crt_time, value])

            # Write the file
            write2file(file_path, array, head=header, delimiter=delimiter)

            # Add to graph
            if self.parent.docks['graph'] is not None:
                self.parent.docks['graph'].thread.addValue(path, array)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------
# Initialise the experiment
def initExperiment(parent, **kwargs):

    # Get the values or the default ones
    name = kwargs.get('name', 'New experiment')
    date_and_time = kwargs.get('date_and_time', None)
    folder = kwargs.get('folder', None)
    comments = kwargs.get('comments', "")

    # Get more specific values for time
    if date_and_time is None:
        date_and_time = date2str( datetime.now() )

    # Get folder
    if folder is None:

        # Get the base folder path
        folder = parent.user_config['save_folder']

        # Use the date if needed
        if parent.user_config['use_date']:
            folder = os.path.join(folder, date_and_time.split(',')[0].replace('/','-'))

        # Add the name of the experiment
        exp_folder_name = name.lower().replace(' ','_')

        # Get the folder
        folder = checkPreviousFolder(folder, exp_folder_name)

    return name, date_and_time, folder, comments

# ----------------------
# Start a new experiment
def setExperiment(parent, **kwargs):

    # Initialise the experiment data if needed
    name, date_and_time, folder, comments = initExperiment( parent, **kwargs )

    # Start the class
    new_experiment = Experiment(parent, name, date_and_time, folder, comments)

    return new_experiment

# ------------------------------
# Create a copy of an experiment
def copyExperiment(parent, experiment):

    # Get the informations
    name = experiment.name
    date_and_time = date2str( datetime.now() )
    folder = experiment.folder
    comments = experiment.comments

    # Update the name and folder
    name_elements = name.split('_copy(')
    if len(name_elements) > 1:
        name_id = int(name_elements[-1].replace(')','')) + 1
    else:
        name_id = 1
    name = name_elements[0] + '_copy(' + str(name_id) + ')'

    folder_dir, folder = os.path.split(folder)
    folder = folder.split('_copy(')[0] + '_copy(' + str(name_id) + ')'
    folder = os.path.join(folder_dir, folder)

    # Start the class
    new_experiment = Experiment(parent, name, date_and_time, folder, comments)

    return new_experiment
