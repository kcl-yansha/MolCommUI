import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

# ---------------------------------
# Combobox with advanced properties
class AdvComboBox(qtw.QComboBox):
    def __init__(self, *args, **kwargs):

        # Call the label
        qtw.QComboBox.__init__(self, *args, **kwargs)

    ##-\-\-\-\
    ## METHODS
    ##-/-/-/-/
    def setTextValue(self, text):

        # Find the index of the text
        index = self.findText(text, qtc.Qt.MatchFixedString)

        # Set the index if found
        if index >= 0:
            self.setCurrentIndex(index)
