###========================================================###
### MolCommUI --- v1.0                                     ###
### Date: 20/02/2023                                       ###
###========================================================###
# Disclaimer: Python3 software developed by the Yansha Group #
#             at King's College London (UK)                  #
# Link: https://www.yanshadeng.org                           #
#------------------------------------------------------------#
# Author(s):                                                 #
# - Vivien WALTER (walter.vivien@gmail.com)                  #
###========================================================###

import sys

import PyQt5.QtWidgets as qtw

from user_interface.main_window.display import mainGUI

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = mainGUI(app)
    sys.exit(app.exec_())
