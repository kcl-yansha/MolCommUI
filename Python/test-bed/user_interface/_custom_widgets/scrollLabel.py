import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## LABEL WITH SCROLLABLE CONTENT
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class ScrollLabel(qtw.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(ScrollLabel, self).__init__()

        # Edit the property of the widget
        self.setWidgetResizable(True)

        # Initialise the widget
        content = qtw.QWidget(self)
        layout = qtw.QVBoxLayout(content)

        # Define the label
        self.label = qtw.QLabel(content)
        self.label.setAlignment( qtc.Qt.AlignLeft | qtc.Qt.AlignTop )

        # Make the label multi-line
        self.label.setWordWrap(True)

        # Add the widget to the layout
        layout.addWidget(self.label)

        # Display the widget
        content.setLayout(layout)
        self.setWidget(content)

    ##-\-\-\-\
    ## METHODS
    ##-/-/-/-/

    # ---------------------
    # Set text to the label
    def setText(self, text):
        self.label.setText(text)

    # --------------------
    # Append text to label
    def appendText(self, text):
        previous_text = self.label.text()
        self.setText(previous_text + text)

    # -------------------
    # Clear text to label
    def clearText(self):
        self.setText("")
