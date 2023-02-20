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
from user_interface._custom_widgets.separators import HorizontalSeparator

from user_interface.groups.syringe_items.functions import SyringeGroupFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class SyringeGroup(qtw.QGroupBox, SyringeGroupFunctions):
    def __init__(self, parent, syringe):
        super(SyringeGroup, self).__init__(parent)

        # Associate the syringe
        self.syringe = syringe
        self.syringe.widget = self

        if self.syringe.equipment.assigned_flowmeter is not None:
            self.flowmeter = self.syringe.equipment.assigned_flowmeter
            self.flowmeter.widget = self
        else:
            self.flowmeter = None

        # Initialise the subwindow
        self.parent = parent
        self.setTitle(self.syringe.name)

        self.layout = qtw.QVBoxLayout(self)

        # Add the content of the window
        self.createSyringePropertiesDisplay( self.layout )
        self.createSyringeActionDisplay( self.layout )
        if self.syringe.equipment.assigned_flowmeter is not None:
            self.layout.addWidget( HorizontalSeparator() )
            self.createSyringeSynchronisationDisplay( self.layout )

        # Display the window
        self.setLayout(self.layout)
        self.setFixedWidth(520)

        if self.syringe.equipment.assigned_flowmeter is not None:
            self.setFixedHeight(230)
            self.displayUnit()
        else:
            self.setFixedHeight(185)

        # Initialise the UI
        self.displaySpeed()
        self.updateRunning()

        # Set the contextual menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightClickMenu)

    ##-\-\-\-\-\-\
    ## GENERATE UI
    ##-/-/-/-/-/-/

    # -----------------------------------------
    # Add the display of the syringe properties
    def createSyringePropertiesDisplay(self, parentWidget):

        # Create the property widget
        self.propertiesWidget = qtw.QWidget()
        self.propertiesLayout = qtw.QGridLayout( self.propertiesWidget )

        currentRow = 0

        # Syringe group
        self.propertiesLayout.addWidget( BoldLabel("Board:"), currentRow, 0 )
        self.boardLabel = qtw.QLabel( self.syringe.syringe_group.name + ' (' + self.syringe.axis + ')' )
        self.propertiesLayout.addWidget( self.boardLabel, currentRow, 1, 1, 4 )

        # Config button
        self.configButton = IconButton(icon_size=35, icon='settings_button.png')
        self.configButton.released.connect(self.openSettings)
        self.configButton.setToolTip("Edit the settings of the syringe pump.")
        self.configButton.setStatusTip("Edit the settings of the syringe pump.")
        self.propertiesLayout.addWidget(self.configButton, currentRow, 5, 2, 1)#, alignment=qtc.Qt.AlignBottom)

        currentRow += 1

        # Syringe group
        #self.propertiesLayout.addWidget( BoldLabel("Speed:"), currentRow, 0 )
        self.speedLabel = qtw.QLabel( "" )
        #self.propertiesLayout.addWidget( self.speedLabel, currentRow, 1 )

        # Syringe group
        #self.propertiesLayout.addWidget( BoldLabel("Acceleration:"), currentRow, 2 )
        self.accelerationLabel = qtw.QLabel( "" )
        #self.propertiesLayout.addWidget( self.accelerationLabel, currentRow, 3 )

        self.propertiesLayout.addWidget( BoldLabel("Current status:"), currentRow, 0, 1 , 2 )

        self.capacityProgressBar = qtw.QProgressBar()
        self.capacityProgressBar.setValue(100)
        self.capacityProgressBar.setFormat("")
        self.capacityProgressBar.setToolTip('Status of the pump. Blue: idle, Green: running')
        self.capacityProgressBar.setStatusTip('Status of the pump. Blue: idle, Green: running')
        self.propertiesLayout.addWidget( self.capacityProgressBar, currentRow, 2 )

        # Make the display
        self.propertiesWidget.setLayout( self.propertiesLayout )
        parentWidget.addWidget( self.propertiesWidget )

    # -----------------------------------------------------------
    # Create the display for the available action for the syringe
    def createSyringeActionDisplay(self, parentWidget):

        # Create the property widget
        self.actionWidget = qtw.QWidget()
        self.actionLayout = qtw.QGridLayout( self.actionWidget )

        crt_row = 0

        # Backward button
        self.runBackButton = IconButton(icon_size=30, icon='start_button_reverse.png')
        self.runBackButton.released.connect(lambda:self.sendRunCommand(direction=-1))
        self.runBackButton.setToolTip("Run the syringe pump backward.")
        self.runBackButton.setStatusTip("Run the syringe pump backward.")
        self.actionLayout.addWidget(self.runBackButton, crt_row, 0, 2, 1)

        # Stop button
        self.stopButton = IconButton(icon_size=30, icon='stop_button.png')
        self.stopButton.released.connect(self.sendStopCommand)
        self.stopButton.setToolTip("Stop the syringe pump.")
        self.stopButton.setStatusTip("Stop the syringe pump.")
        self.actionLayout.addWidget(self.stopButton, crt_row, 1, 2, 1)

        # Run button
        self.runButton = IconButton(icon_size=30, icon='start_button.png')
        self.runButton.released.connect(self.sendRunCommand)
        self.runButton.setToolTip("Run the syringe pump forward.")
        self.runButton.setStatusTip("Run the syringe pump forward.")
        self.actionLayout.addWidget(self.runButton, crt_row, 2, 2, 1)

        # Volume entry
        self.actionLayout.addWidget( BoldLabel("Volume:"), crt_row, 3 )

        self.volumeEntry = qtw.QLineEdit()
        self.volumeEntry.setText( self.syringe.equipment.set_volume_text )
        self.volumeEntry.setFixedWidth(75)
        self.volumeEntry.setToolTip('Total volume to inject')
        self.volumeEntry.setStatusTip('Total volume to inject')
        self.volumeEntry.editingFinished.connect(self.updateVolumeSlider)
        self.actionLayout.addWidget(self.volumeEntry, crt_row, 4)

        self.actionLayout.addWidget( qtw.QLabel("µL"), crt_row, 5 )

        # Volume entry
        self.volumeSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setFixedWidth(175)
        self.volumeSlider.setToolTip('Select the total volume to inject')
        self.volumeSlider.setStatusTip('Select the total volume to inject')
        self.volumeSlider.sliderMoved.connect(self.updateVolumeEntry)
        self.actionLayout.addWidget(self.volumeSlider, crt_row, 6)

        self.updateVolumeSlider()

        crt_row += 1

        # Volume entry
        self.actionLayout.addWidget( BoldLabel("Flow rate:"), crt_row, 3 )

        self.speedEntry = qtw.QDoubleSpinBox()
        self.speedEntry.setDecimals(4)
        self.speedEntry.setMaximum(10000)
        self.speedEntry.setFixedWidth(125)
        self.speedEntry.setToolTip('Flow rate to apply to the pump')
        self.speedEntry.setStatusTip('Flow rate to apply to the pump')
        self.actionLayout.addWidget(self.speedEntry, crt_row, 4, 1, 2)

        self.speedUnitLabel = qtw.QLabel("")
        self.actionLayout.addWidget( self.speedUnitLabel, crt_row, 6)

        self.setSpeedButton = qtw.QPushButton('Set')
        self.setSpeedButton.setToolTip('Apply the selected flow rate to the pump')
        self.setSpeedButton.setStatusTip('Apply the selected flow rate to the pump')
        self.setSpeedButton.released.connect(self.sendSetSpeedCommand)
        self.actionLayout.addWidget(self.setSpeedButton, crt_row, 7)

        # Make the display
        self.actionWidget.setLayout( self.actionLayout )
        parentWidget.addWidget( self.actionWidget, alignment=qtc.Qt.AlignLeft )

    # ------------------------------------------
    # Create the display for the synchronisation
    def createSyringeSynchronisationDisplay(self, parentWidget):

        # Create the property widget
        self.synchronisationWidget = qtw.QWidget()
        self.synchronisationLayout = qtw.QHBoxLayout( self.synchronisationWidget )

        # Config button
        self.synchronisationLayout.addWidget( BoldLabel('Flowmeter:') )#, alignment=qtc.Qt.AlignBottom)

        # Start reading button
        self.startFlowButton = IconButton(icon_size=25, icon='stop_button.png')
        self.startFlowButton.released.connect(self.sendStopReadCommand)
        self.startFlowButton.setToolTip("Stop live measurement.")
        self.startFlowButton.setStatusTip("Stop live measurement.")
        self.synchronisationLayout.addWidget(self.startFlowButton)

        # Stop reading button
        self.stopFlowButton = IconButton(icon_size=25, icon='start_button.png')
        self.stopFlowButton.released.connect(self.sendStartReadCommand)
        self.stopFlowButton.setToolTip("Start live measurement.")
        self.stopFlowButton.setStatusTip("Start live measurement.")
        self.synchronisationLayout.addWidget(self.stopFlowButton)

        # Volume entry
        self.synchronisationLayout.addWidget( qtw.QLabel("Current speed:"), alignment=qtc.Qt.AlignRight )

        self.flowRateDisplay = qtw.QLineEdit("")
        self.flowRateDisplay.setFixedWidth(160)
        self.flowRateDisplay.setToolTip("Flow rate measured at the flow meter.")
        self.flowRateDisplay.setStatusTip("Flow rate measured at the flow meter.")
        self.synchronisationLayout.addWidget(self.flowRateDisplay)

        # Display the speed unit
        self.flowUnitLabel = qtw.QLabel("µL/min")
        self.synchronisationLayout.addWidget( self.flowUnitLabel )

        # Infos button
        self.infoButton = IconButton(icon_size=25, icon='settings_button.png')
        self.infoButton.released.connect(self.openFlowmeterSettings)
        self.infoButton.setToolTip("Edit the settings of the flow meter.")
        self.infoButton.setStatusTip("Edit the settings of the flow meter.")
        self.synchronisationLayout.addWidget(self.infoButton)

        # Make the display
        self.synchronisationWidget.setLayout( self.synchronisationLayout )
        parentWidget.addWidget( self.synchronisationWidget, alignment=qtc.Qt.AlignLeft )

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
