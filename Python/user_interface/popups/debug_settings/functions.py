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
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class debugSettingsFunctions(object):

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------
    # Apply all the changes
    def saveDebugSettings(self):

        # Update the main settings - Syringe pumps
        self.parent.editConfig( 'debug_syringe_send', self.syringeSendCommandCheckbox.isChecked(), from_user=False )
        for syringe in self.parent.equipments['syringe_pumps']:
            syringe.debug = self.syringeSendCommandCheckbox.isChecked()

        self.parent.editConfig( 'debug_syringe', self.syringeVerboseCheckbox.isChecked(), from_user=False )
        for syringe in self.parent.equipments['syringe_pumps']:
            syringe.verbose = self.syringeVerboseCheckbox.isChecked()

        # Update the main settings - Flow meter
        self.parent.editConfig( 'debug_flowmeter', self.flowMeterVerboseCheckbox.isChecked(), from_user=False )
        for flowmeter in self.parent.equipments['flow_meter']:
            flowmeter.debug = self.flowMeterVerboseCheckbox.isChecked()

        # Close the windows
        self.close()
