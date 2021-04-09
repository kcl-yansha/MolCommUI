import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.path_to_assets import getIcon

from user_interface.groups.group_interface.functions import EquipmentGroupsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class EquipmentGroups(qtw.QScrollArea, EquipmentGroupsFunctions):
    def __init__(self, parent):
        super(EquipmentGroups, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.groups = []
        self.groups_widget = []

        # Edit the property of the widget
        self.setWidgetResizable(True)

        # Initialise the widget
        self.content = qtw.QWidget(self)
        self.layout = qtw.QVBoxLayout(self.content)

        # Accept drag and drop events
        self.setAcceptDrops(True)

        # Display the widget
        self.content.setLayout(self.layout)
        self.setWidget(self.content)

    ##-\-\-\-\-\-\-\-\-\
    ## UI INITIALISATION
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------------------------
    # Create the general scrollable display to host the groups
    def createScrollableDisplay(self, parentWidget):

        self.groups = []

        from user_interface.groups.sync_group.display import SynchronisedGroup
        from user_interface.groups.syringe_items.display import SyringeGroup

        crt_widget = SynchronisedGroup(self.parent, title='Group 0')
        parentWidget.addWidget( crt_widget )
        self.groups.append([crt_widget, 'sync_group'])

        for i in range(3):
            crt_widget = SyringeGroup(self.parent, title='Box '+str(i))
            parentWidget.addWidget( crt_widget )
            self.groups.append([crt_widget, 'syringe_pump'])
