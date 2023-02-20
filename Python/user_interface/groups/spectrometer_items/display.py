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

from user_interface._custom_widgets.icon_buttons import IconButton
from user_interface._custom_widgets.customLabel import BoldLabel

from user_interface.groups.spectrometer_items.functions import SpectroMeterGroupFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class SpectroMeterGroup(qtw.QGroupBox, SpectroMeterGroupFunctions):
    def __init__(self, parent, spectrometer):
        super(SpectroMeterGroup, self).__init__(parent)

        # Associate the flow meter
        self.spectrometer = spectrometer
        self.spectrometer.widget = self

        # Initialise the subwindow
        self.parent = parent
        self.setTitle( self.spectrometer.name + ' (' + self.spectrometer.model + ')' )

        self.layout = qtw.QVBoxLayout(self)

        # Add the content of the window
        self.createSpectrometerActionDisplay( self.layout )
        self.createSpectrometerCapacityDisplay( self.layout )

        # Display the window
        self.setLayout(self.layout)
        self.setFixedWidth(520)
        self.setFixedHeight(150)

        # Set the contextual menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightClickMenu)

    ##-\-\-\-\-\-\
    ## GENERATE UI
    ##-/-/-/-/-/-/

    # -------------------------------------------------------------
    # Create the display for the available action for the flowmeter
    def createSpectrometerActionDisplay(self, parentWidget):

        # Create the property widget
        self.actionWidget = qtw.QWidget()
        self.actionLayout = qtw.QHBoxLayout( self.actionWidget )

        # Stop button
        self.stopButton = IconButton(icon_size=25, icon='stop_button.png')
        self.stopButton.released.connect(self.sendStopCommand)
        self.stopButton.setToolTip("Stop the live measurement.")
        self.stopButton.setStatusTip("Stop the live measurement.")
        self.actionLayout.addWidget(self.stopButton)

        # Run button
        self.readButton = IconButton(icon_size=25, icon='start_button.png')
        self.readButton.released.connect(self.sendReadCommand)
        self.readButton.setToolTip("Start the live measurement.")
        self.readButton.setStatusTip("Start the live measurement.")
        self.actionLayout.addWidget(self.readButton)

        # Add spacing
        spacingWidget = qtw.QLabel("")
        spacingWidget.setFixedWidth(60)
        self.actionLayout.addWidget( spacingWidget )

        self.statusDisplay = qtw.QLabel("< Not scanning >")
        self.updateStatus()
        self.actionLayout.addWidget(self.statusDisplay)

        # Make the display
        self.actionWidget.setLayout( self.actionLayout )
        parentWidget.addWidget( self.actionWidget, alignment=qtc.Qt.AlignLeft )

    # ------------------------------------------------
    # Create the display for the spectrometer capacity
    def createSpectrometerCapacityDisplay(self, parentWidget):

        # Create the property widget
        self.capacityWidget = qtw.QWidget()
        self.capacityLayout = qtw.QHBoxLayout( self.capacityWidget )

        # Config button
        self.graphButton = IconButton(icon_size=35, icon='plot_button.png')
        self.graphButton.released.connect(self.openGraph)
        self.graphButton.setToolTip("Display the graph of the spectrometer.")
        self.graphButton.setStatusTip("Display the graph of the spectrometer.")
        self.capacityLayout.addWidget(self.graphButton )#, alignment=qtc.Qt.AlignBottom)

        # Config button
        self.configButton = IconButton(icon_size=35, icon='settings_button.png')
        self.configButton.released.connect(self.openSettings)
        self.configButton.setToolTip("Edit the settings of the spectrometer.")
        self.configButton.setStatusTip("Edit the settings of the spectrometer.")
        self.capacityLayout.addWidget(self.configButton )#, alignment=qtc.Qt.AlignBottom)

        # Make the display
        self.capacityWidget.setLayout( self.capacityLayout )
        parentWidget.addWidget( self.capacityWidget, alignment=qtc.Qt.AlignLeft )

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## DEFINE THE DRAG & DROP ACTION
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------------
    # Get the mouse event
    def mouseMoveEvent(self, event):
        if event.buttons() == qtc.Qt.LeftButton:
            mimeData = qtc.QMimeData()
            drag = qtg.QDrag(self)
            drag.setMimeData(mimeData)
            dropAction = drag.exec_(qtc.Qt.MoveAction)
