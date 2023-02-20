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

from user_interface.groups.flowmeter_items.functions import FlowMeterGroupFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class FlowMeterGroup(qtw.QGroupBox, FlowMeterGroupFunctions):
    def __init__(self, parent, flowmeter):
        super(FlowMeterGroup, self).__init__(parent)

        # Associate the flow meter
        self.flowmeter = flowmeter
        self.flowmeter.widget = self

        # Initialise the subwindow
        self.parent = parent
        self.setTitle( self.flowmeter.name + ' (' + self.flowmeter.ftype + ')' )

        self.layout = qtw.QVBoxLayout(self)

        # Add the content of the window
        self.createFlowmeterActionDisplay( self.layout )
        self.createFlowmeterCapacityDisplay( self.layout )

        # Display the window
        self.setLayout(self.layout)
        self.setFixedWidth(520)
        self.setFixedHeight(150)

        # Initialise the UI
        self.displayUnit()

        # Set the contextual menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightClickMenu)

    ##-\-\-\-\-\-\
    ## GENERATE UI
    ##-/-/-/-/-/-/

    # -------------------------------------------------------------
    # Create the display for the available action for the flowmeter
    def createFlowmeterActionDisplay(self, parentWidget):

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
        self.spacingWidget = qtw.QLabel("")
        self.spacingWidget.setFixedWidth(60)
        self.actionLayout.addWidget( self.spacingWidget )

        # Volume entry
        self.actionLayout.addWidget( qtw.QLabel("Current speed:"), alignment=qtc.Qt.AlignRight )

        self.speedDisplay = qtw.QLineEdit("")
        self.speedDisplay.setFixedWidth(200)
        self.speedDisplay.setToolTip("Flow rate measured at the flow meter.")
        self.speedDisplay.setStatusTip("Flow rate measured at the flow meter.")
        self.actionLayout.addWidget(self.speedDisplay)

        # Display the speed unit
        self.speedLabel = qtw.QLabel("µL/min")
        self.actionLayout.addWidget( self.speedLabel )

        # Make the display
        self.actionWidget.setLayout( self.actionLayout )
        parentWidget.addWidget( self.actionWidget )#, alignment=qtc.Qt.AlignLeft )

    # ---------------------------------------------
    # Create the display for the flowmeter capacity
    def createFlowmeterCapacityDisplay(self, parentWidget):

        # Create the property widget
        self.capacityWidget = qtw.QWidget()
        self.capacityLayout = qtw.QHBoxLayout( self.capacityWidget )

        # Config button
        self.configButton = IconButton(icon_size=35, icon='settings_button.png')
        self.configButton.released.connect(self.openSettings)
        self.configButton.setToolTip("Edit the settings of the flowmeter.")
        self.configButton.setStatusTip("Edit the settings of the flowmeter.")
        self.capacityLayout.addWidget(self.configButton )#, alignment=qtc.Qt.AlignBottom)

        # Display the progress bar
        self.capacityProgressBar = qtw.QProgressBar(textVisible=False)
        self.capacityProgressBar.setFixedWidth(250)
        self.setBarRange()
        self.capacityProgressBar.setToolTip('Capacity of the flow meter')
        self.capacityProgressBar.setStatusTip('Capacity of the flow meter')
        self.capacityLayout.addWidget( self.capacityProgressBar, alignment=qtc.Qt.AlignRight )

        # Make the display
        self.capacityWidget.setLayout( self.capacityLayout )
        parentWidget.addWidget( self.capacityWidget )

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
