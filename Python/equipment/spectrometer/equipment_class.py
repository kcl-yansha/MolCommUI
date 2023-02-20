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
import time

from equipment.spectrometer.calculation import getAbsorbance, rescaleIntensity
from equipment.spectrometer.commands import start_connection, stop_connection, get_spectrometer_infos, set_integration_time, get_measurement

from multithreading.threads.spectrometer_comm import SpectroMeterThread

##-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS FOR A SINGLE PUMP
##-/-/-/-/-/-/-/-/-/-/-/-/

class SpectroMeter:
    def __init__(self, parent, spectrometer, serial_number, debug=True):

        # General properties
        self.name = "Spectrometer"
        self.serial_number = serial_number
        self.spectrometer = spectrometer

        self.parent = parent
        self.widget = None

        self.debug = debug
        self.integration_time = 50 # value in ms
        self.delay_time = 100 # value in ms

        # Spectrometer status
        self.is_running = False
        self.read_values = False

        # Spectrometer values
        self.wavelengths = None
        self.last_values = None

        # Main thread
        self.thread = SpectroMeterThread(self)
        self.thread.signals.result.connect(self.getChange)
        self.thread.signals.finished.connect(self._close_connection)
        self.thread.start()

        # Prepare for saving data
        self.file_name = "untitled"
        self.header = {'comments':[], 'header':[]}
        self.since_last = 0

        # Display and calculations values
        self.baseline = None
        self.rescaled = None
        self.absorption = None

        self.w_rescale = 500
        self.w_concentration = 629

        # Initialise the instance
        self.getSpectrometerInfos()
        self.getFileInfos()

    ##-\-\-\-\-\-\-\-\
    ## GENERAL METHODS
    ##-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Get the information on the spectrometer
    def getSpectrometerInfos(self):

        # Request the details
        spectro_dict = get_spectrometer_infos(self.spectrometer)

        # Save the values
        self.model = spectro_dict['model']
        self.n_pixels = spectro_dict['pixels']

    # --------------------------------
    # Close the connecton to the group
    def close(self):
        self.thread.interrupt()

    # ---------------------------------
    # Close the connection to the board
    def _close_connection(self):
        stop_connection(self.spectrometer)

    # ------------------------------
    # Get the header for file saving
    def getFileInfos(self):

        # Define the name of the file to save
        self.file_name = self.serial_number.replace('/','') + '_' + self.name.lower().replace(' ','')

        # Get the column names
        columns = ['Time (s)']

        # Build the column name
        spectrum = get_measurement(self.spectrometer, intensity_only=False, debug=self.debug)
        self.wavelengths = spectrum[0]
        self.last_values = spectrum[1]

        for wv in spectrum[0]:
            columns.append(str(wv)+' (nm)')

        # Get the informations
        infos = [
        'Spectrometer: '+self.name,
        'Serial Number: '+str(self.serial_number),
        'Model: '+str(self.model),
        'Number of Pixels: '+str(self.n_pixels)
        ]

        # Make the dictionary
        self.header = {'comments':infos, 'header':columns}

    ##-\-\-\-\-\-\-\-\-\-\
    ## THREAD COMMUNICATION
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------
    # Enqueue the next command
    def enqueue(self, event_type, fn, *args, **kwargs):
        self.thread.queue.enqueue( self.serial_number, event_type, fn, *args, **kwargs )

    # ------------------------------
    # Get the change from the thread
    def getChange(self, value):

        # Save the last values
        self.last_values = value

        # Do another measurement
        if self.read_values:
            self.read()

        # Write to file in the experiment
        if time.time() - self.since_last > self.delay_time/1000:
            self.parent.experiment.save(self.file_name, value, header=self.header)
            self.since_last = time.time()

        # Update the UI
        if self.widget is not None:
            self.widget.updateStatus()

        # Add to graph
        if self.parent.docks['spectrum'] is not None:
            self.parent.docks['spectrum'].refreshSpectrum(self)

    ##-\-\-\-\-\-\-\-\
    ## GRAPHIC DISPLAY
    ##-/-/-/-/-/-/-/-/

    # --------------
    # Get a baseline
    def setBaseline(self):
        self.baseline = np.copy( self.last_values )

    # -------------------
    # Update the spectrum
    def updateSpectrum(self):

        # Absorption spectrum
        if self.baseline is not None:

            self.rescaled = rescaleIntensity(self.wavelengths, self.last_values, self.baseline, self.w_rescale)
            self.absorption = getAbsorbance(self.rescaled, self.baseline)

    ##-\-\-\-\
    ## COMMANDS
    ##-/-/-/-/

    # --------------------------------------------
    # Set the integration time of the spectrometer
    def setIntegrationTime(self, value):

        # Convert value
        value = int(value)

        # Save value
        self.integration_time = value

        # Send the value (in microseconds)
        set_integration_time(self.spectrometer, value * 1000 / 2, debug=self.debug)

    # ------------------------
    # Read the flowmeter value
    def read(self):
        self.enqueue('read', get_measurement, self.spectrometer, debug=self.debug)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

# --------------------------------------------------
# Load the spectrometer with the given serial number
def loadSpectroMeterClass(parent, serial_number, debug=False):

    # Open the port to check it
    spectrometer_unit = start_connection(serial_number)

    # Check that the port opening was successful
    if spectrometer_unit is not None:
        print('Connected to Spectrometer')
        print('-------------------------')

        # Initialise the class
        new_class = SpectroMeter(parent, spectrometer_unit, serial_number, debug=debug)

        try:

            # Set the integration time of the spectrometer to a default of 100 ms
            new_class.setIntegrationTime(50)

            return new_class

        # Raise an error if the commands cannot be sent
        except:

            # Stop the connection to the board
            stop_connection(spectrometer_unit)

            return None

    # Return an empty class if nothing worked
    return None
