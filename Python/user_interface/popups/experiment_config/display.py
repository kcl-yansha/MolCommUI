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

from input_output.misc import str2date
from input_output.experiments.experiment_class import setExperiment
from equipment.flow_meter.properties import getFlowMeterType

from user_interface._custom_widgets.customLabel import BoldLabel
from user_interface._custom_widgets.browse import Browse
from user_interface._custom_widgets.buttons import AcceptButton, CancelButton
from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.popups.experiment_config.functions import setExperimentFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class setExperimentWindow(qtw.QMainWindow, setExperimentFunctions):
    def __init__(self, parent, experiment=None):
        super(setExperimentWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setStatusBar(qtw.QStatusBar())

        # Load the experiment
        if experiment is None:
            self.experiment = setExperiment(self.parent)
        else:
            self.experiment = experiment

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Manage Experiment")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Populate the panel
        self.createExpNameDisplay(self.mainLayout)
        self.mainLayout.addWidget( HorizontalSeparator() )
        self.createExpDetailsDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(qtc.QSize(550, 400))

        # Initialise the appearance of the button
        #self.updateConnectButton()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the window
        event.accept()
        self.parent.subWindows['experiment'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------
    # Generate the name selection
    def createExpNameDisplay(self, parentWidget):

        # Generate the widget
        self.experimentNameWidget = qtw.QWidget()
        self.experimentNameLayout = qtw.QHBoxLayout(self.experimentNameWidget)

        # Add the entry for the experiment name
        self.experimentNameLayout.addWidget( BoldLabel("Name:") )

        self.nameEntry = qtw.QLineEdit()
        self.nameEntry.setText( self.experiment.name )
        self.nameEntry.setToolTip("Name of the experiment")
        self.nameEntry.setStatusTip("Name of the experiment")
        self.experimentNameLayout.addWidget( self.nameEntry )

        # Display the widget
        self.experimentNameWidget.setLayout(self.experimentNameLayout)
        parentWidget.addWidget(self.experimentNameWidget)

    # ------------------------------
    # Generate the information entry
    def createExpDetailsDisplay(self, parentWidget):

        # Generate the widget
        self.experimentDetailsWidget = qtw.QWidget()
        self.experimentDetailsLayout = qtw.QGridLayout(self.experimentDetailsWidget)

        crt_row = 0

        # Date input
        self.experimentDetailsLayout.addWidget( BoldLabel("Date/Time:"), crt_row, 0 )

        self.dateEntry = qtw.QDateTimeEdit(calendarPopup=True)
        self.dateEntry.setDateTime( str2date( self.experiment.date_and_time, qt=True ) )
        self.dateEntry.setToolTip("Time and date at which the experiment started")
        self.dateEntry.setStatusTip("Time and date at which the experiment started")
        self.experimentDetailsLayout.addWidget( self.dateEntry, crt_row, 1 )

        crt_row += 1

        # Experiment folder selection
        self.experimentDetailsLayout.addWidget( BoldLabel("Experiment folder:"), crt_row, 0, 1 ,2 )

        crt_row += 1

        self.folderBrowsing = Browse()
        self.folderBrowsing.setText( self.experiment.folder )
        self.folderBrowsing.connectButton(self.browsePath)
        self.folderBrowsing.setToolTip("Browse to select the folder in which to save the experiment")
        self.folderBrowsing.setStatusTip("Browse to select the folder in which to save the experiment")
        self.experimentDetailsLayout.addWidget( self.folderBrowsing, crt_row, 0, 1 ,2 )

        crt_row += 1

        # Comments entry
        self.experimentDetailsLayout.addWidget( BoldLabel("Comments:"), crt_row, 0, 1 ,2 )

        crt_row += 1

        self.commentEntry = qtw.QPlainTextEdit()
        self.commentEntry.setFixedHeight(100)
        self.commentEntry.setPlainText( self.experiment.comments )
        self.commentEntry.setToolTip("Additional comments on the experiment")
        self.commentEntry.setStatusTip("Additional comments on the experiment")
        self.experimentDetailsLayout.addWidget( self.commentEntry, crt_row, 0, 1 ,2 )

        # Display the widget
        self.experimentDetailsWidget.setLayout(self.experimentDetailsLayout)
        parentWidget.addWidget(self.experimentDetailsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.setButton = AcceptButton("Set")
        self.setButton.clicked.connect(self.saveExperimentDetails)
        self.setButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.setButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = CancelButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
