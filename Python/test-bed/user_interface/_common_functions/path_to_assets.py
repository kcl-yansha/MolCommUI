import os

import PyQt5.QtGui as qtg

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTION
##-/-/-/-/-/-/-/-/

# ------------------------
# Get the path to the icon
def getIcon(icon_file):
    return qtg.QIcon( os.path.join('user_interface','_icons',icon_file) )
