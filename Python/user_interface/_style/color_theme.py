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

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from user_interface._style.proxy_style import ProxyStyle

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------
# Apply the Fusion style
def _fusion_style(app):

    # Select the style to use
    app.setStyle("Fusion")

    # Add the proxy style
    proxy_style = ProxyStyle(app.style())
    app.setStyle(proxy_style)

    # Generate the colour palette
    palette = qtg.QPalette() # Get a copy of the standard palette.

    # Define colours
    background = qtg.QColor(40, 50, 60)
    button = qtg.QColor(55, 80, 95)
    button_disabled = qtg.QColor('#4a6c82')
    light_background = qtg.QColor(30, 35, 45)
    links = qtg.QColor(42, 130, 218)
    highlight = qtg.QColor(60, 123, 150)
    tooltip_background = qtg.QColor(91, 160, 190)

    palette.setColor(qtg.QPalette.Window, background)
    palette.setColor(qtg.QPalette.WindowText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Base, light_background)
    palette.setColor(qtg.QPalette.AlternateBase, background)
    palette.setColor(qtg.QPalette.ToolTipBase, tooltip_background)#qtc.Qt.white)
    palette.setColor(qtg.QPalette.ToolTipText, qtc.Qt.black)
    palette.setColor(qtg.QPalette.Text, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Button, button)
    palette.setColor(qtg.QPalette.Disabled, qtg.QPalette.Button, button_disabled)
    palette.setColor(qtg.QPalette.ButtonText, qtc.Qt.white)
    palette.setColor(qtg.QPalette.Disabled, qtg.QPalette.ButtonText, qtc.Qt.gray)
    palette.setColor(qtg.QPalette.BrightText, qtc.Qt.red)
    palette.setColor(qtg.QPalette.Link, links)
    palette.setColor(qtg.QPalette.Highlight, highlight)
    palette.setColor(qtg.QPalette.HighlightedText, qtc.Qt.black)

    # Set the palette
    app.setPalette(palette)

    # Additional CSS styling for tooltip elements.
    #app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------
# Apply the required style to the GUI
def applyStyle( app, style='fusion' ):

    # Select the style to apply
    if style == 'fusion':
        _fusion_style(app)
