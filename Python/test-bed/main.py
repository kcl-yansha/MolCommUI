import sys

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface.main_window.display import mainGUI

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    #app.setWindowIcon(qtg.QIcon('icon.ico')) # Uncomment to add an icon
    main_window = mainGUI(app)
    sys.exit(app.exec_())
