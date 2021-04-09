import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._common_functions.path_to_assets import getIcon

class IconButton(qtw.QToolButton):
    def __init__(self, *args, **kwargs):

        # Get the extra parameters
        size = kwargs.pop('icon_size',20)
        icon = kwargs.pop('icon', 'previous_button.png')

        # Call the label
        qtw.QToolButton.__init__(self, *args, **kwargs)

        # Set the icon
        self.setIcon( getIcon(icon) )

        # Set the size
        self.setFixedSize(size,size)
        self.setIconSize(qtc.QSize(size*.8,size*.8))

    ##-\-\-\-\
    ## METHODS
    ##-/-/-/-/

    # -----------------
    # Resize the button
    def setSize(self, size):

        self.setFixedSize(size,size)
        self.setIconSize(qtc.QSize(size,size))
