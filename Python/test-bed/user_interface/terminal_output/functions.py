import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from multithreading.streams.terminal_stream import EmittingStream

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class TerminalOutputFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\
    ## TERMINAL REDIRECTION
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------------------------
    # Catch the output of the terminal and display it in the label
    def catchTerminal(self, event=None):

        # Redirect the terminal output
        sys.stdout = EmittingStream( textWritten = self.writeTerminalOutput )

    # ---------------------------------------------
    # Write the output of the terminal in the label
    def writeTerminalOutput(self, text):
        self.terminalOutputLabel.appendText(text)
