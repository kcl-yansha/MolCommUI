import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.path_to_assets import getIcon
from user_interface._custom_widgets.customLabel import ItalicLabel

from user_interface.groups.sync_group.functions import SynchronisedGroupFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class SynchronisedGroup(qtw.QGroupBox, SynchronisedGroupFunctions):
    def __init__(self, parent, title='Untitled'):
        super(SynchronisedGroup, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setTitle(title)
        self.empty = True

        # Add some design
        self.setObjectName('SyncGroup')
        self.setStyleSheet('QGroupBox#SyncGroup { margin-top:8px; border: 1.5px dashed white; border-radius: 5px; } QGroupBox#SyncGroup::title { subcontrol-origin: margin; subcontrol-position: top; padding: 0px 5px 0px 5px; }')

        # Initialise the widget
        self.layout = qtw.QVBoxLayout(self)

        self.createEmptyMessage(self.layout)

        self.setLayout(self.layout)

        # Set the contextual menu
        self.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightClickMenu)

    ##-\-\-\-\-\-\-\
    ## UI GENERATION
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Create the empty message label
    def createEmptyMessage(self, parentWidget):

        # Display the text
        label = ItalicLabel('The group is empty. Drag and drop equipment in the group to synchronise them.')
        self.layout.addWidget(label)

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
