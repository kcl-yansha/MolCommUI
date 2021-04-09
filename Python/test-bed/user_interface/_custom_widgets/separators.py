import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## COMMON SECTION SEPARATORS
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# ---------------------------
# Define the separator widget
def HorizontalSeparator():
    separator = qtw.QFrame()
    separator.setFrameShape(qtw.QFrame.HLine)
    separator.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
    separator.setLineWidth(1)

    return separator

# ---------------------------
# Define the separator widget
def VerticalSeparator():
    separator = qtw.QFrame()
    separator.setFrameShape(qtw.QFrame.VLine)
    separator.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
    separator.setLineWidth(1)

    return separator
