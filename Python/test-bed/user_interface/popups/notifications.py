import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## GENERIC ERROR AND WARNING
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# -----------------------------------------------------------
# Display a warning message box with a user choice to proceed
def warningProceedMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)

    # Add the informations
    msg.setWindowTitle('WARNING')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
    retval = msg.exec_()

    return retval == qtw.QMessageBox.Ok

# -----------------------------
# Display a warning message box
def warningMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)

    # Add the informations
    msg.setWindowTitle('WARNING')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

    return retval == qtw.QMessageBox.Ok

# ------------------------------------------------
# Display an error message with a single OK button
def errorMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)

    # Add the informations
    msg.setWindowTitle('ERROR')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

# -------------------------------------------------
# Display a notification message to inform the user
def notificationMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)

    # Add the informations
    msg.setWindowTitle('INFO(S)')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()
