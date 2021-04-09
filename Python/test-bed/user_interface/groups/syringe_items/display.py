import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.path_to_assets import getIcon

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class SyringeGroup(qtw.QGroupBox):
    def __init__(self, parent, title='Untitled'):
        super(SyringeGroup, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setTitle(title)

        self.layout = qtw.QVBoxLayout(self)

        label = qtw.QLabel('Miaou')
        self.layout.addWidget(label)

        test = qtw.QPushButton('Here')
        self.layout.addWidget(test)

        self.setLayout(self.layout)

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
