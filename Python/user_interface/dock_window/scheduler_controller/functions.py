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

from functools import partial

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from user_interface._custom_widgets.customLabel import BoldLabel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class SchedulerControllerFunctions(object):

    ##-\-\-\-\-\
    ## UPDATE UI
    ##-/-/-/-/-/

    # -----------------
    # Update the status
    def updateStatus(self, status):

        # Bold
        boldfont = qtg.QFont()
        boldfont.setBold(True)

        # Normal
        normalfont = qtg.QFont()
        normalfont.setBold(False)

        # Change to ON
        if status:
            self.schedulerStatusOn.setStyleSheet("color: #247E5C")
            self.schedulerStatusOn.setFont(boldfont)

            self.schedulerStatusOff.setStyleSheet("color: #36454e")
            self.schedulerStatusOff.setFont(normalfont)

        # Change to OFF
        else:
            self.schedulerStatusOn.setStyleSheet("color: #36454e")
            self.schedulerStatusOn.setFont(normalfont)

            self.schedulerStatusOff.setStyleSheet("color: #8C2E2E")
            self.schedulerStatusOff.setFont(boldfont)

    # -----------------
    # Update the status
    def updateNote(self, note=None, next=None):

        # Get current note
        if note is None:
            text = 'Current: None'
        else:
            text = 'Current: '+str(note)

        # Get next note
        if next is None:
            next_text = 'Next: None'
        else:
            next_text = 'Next: '+str(next)

        self.schedulerNote.setText(text)
        self.schedulerPastNote.setText(next_text)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # --------------------
    # Toggle the scheduler
    def toggleScheduler(self):

        # Check the status
        if self.parent.scheduler_running:
            self.parent.stopScheduler()

        else:
            self.parent.startScheduler()
