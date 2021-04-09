import PyQt5.QtCore as qtc

# ------------------------------------------------------------
# Define the class to emit signal when data is written into it
class EmittingStream(qtc.QObject):

    # Define the list of signals
    textWritten = qtc.pyqtSignal(str)

    # Write text into the stream
    def write(self, text):

        # Emit the signal
        self.textWritten.emit(str(text))
