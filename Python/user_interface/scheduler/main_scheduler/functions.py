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
import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from input_output.scheduler import fileToScheduler, schedulerToFile

import multithreading.scheduler.events as scd

from user_interface._custom_widgets.icon_buttons import IconButton

from user_interface._common_functions.window_handling import openWindow

from user_interface.popups.notifications import warningMessage, warningProceedMessage, errorMessage

from user_interface.dock_window.scheduler_controller.display import SchedulerControllerPanel

from user_interface.scheduler.assign_pumps.display import assignPumpWindow
from user_interface.scheduler.constant.display import setConstantWindow
from user_interface.scheduler.experiment_toggle.display import setExperimentToggleWindow
from user_interface.scheduler.stop.display import setStopWindow
from user_interface.scheduler.wait.display import setWaitWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class setSchedulerFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, event):

        # Fill the rows
        self.eventTable.insertRow(i)

        # Make the buttons
        upButton = IconButton(icon_size=30, icon='up_button.png')
        upButton.released.connect(partial(self.moveEventUp, event_id=i))
        upButton.setToolTip("Move the event up.")

        downButton = IconButton(icon_size=30, icon='down_button.png')
        downButton.released.connect(partial(self.moveEventDown, event_id=i))
        downButton.setToolTip("Move the event down.")

        eventEditButton = IconButton(icon_size=30, icon='settings_button.png')
        eventEditButton.released.connect(partial(self.editEvent, event_id=i))
        eventEditButton.setToolTip("Edit the parameters of the event.")

        eventDeleteButton = IconButton(icon_size=30, icon='delete_button.png')
        eventDeleteButton.released.connect(partial(self.deleteEvent, event_id=i))
        eventDeleteButton.setToolTip("Delete the event.")

        # Fill the columns
        self.eventTable.setCellWidget(i, 0, upButton)
        self.eventTable.setCellWidget(i, 1, downButton)

        self.eventTable.setItem(i, 2,  qtw.QTableWidgetItem( event.description ))

        self.eventTable.setCellWidget(i, 3, eventEditButton)
        self.eventTable.setCellWidget(i, 4, eventDeleteButton)

        self.eventTable.setItem(i, 5,  qtw.QTableWidgetItem( event.pump_desc ))

    # ------------------
    # Populate the table
    def fillEventTable(self):

        # Reinialise the table
        self.eventTable.reset()

        # Fill the table
        i = -1
        if len(self.events) > 0:
            for i, event in enumerate(self.events):
                self._make_row(i, event)

        # Resize the columns
        self.eventTable.resizeCols()

    ##-\-\-\-\-\-\-\-\
    ## MANAGE ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ------------------------
    # Add an event to the list
    def addEvent(self, event):

        if len(self.events) == 0:
            self.events.append(event)

        else:
            if self.events[-1].event_type == 'Repeat':
                self.events.insert(-1, event)

            else:
                self.events.append(event)

    # ------------------------------
    # Delete the selected controller
    def deleteEvent(self, event_id=0):

        # Ask the user to confirm first
        if warningProceedMessage('Delete the event?','Are you sure you want to delete the selected event?'):

            # Delete the selection
            self.events.pop(event_id)

            # Reload the table
            self.fillEventTable()

    # -----------------------
    # Edit the selected event
    def editEvent(self, event_id=0):

        # Get the event
        crt_event = self.events[event_id]

        if crt_event.event_type == 'Constant':
            self.editConstant(event=crt_event)

        elif crt_event.event_type == 'Stop':
            self.editStop(event=crt_event)

        elif crt_event.event_type == 'Wait':
            self.editWait(event=crt_event)

        elif crt_event.event_type == 'ToggleExp':
            self.editExperimentToggle(event=crt_event)

    # ----------------------------
    # Modify the selected constant
    def editConstant(self, event=None):
        openWindow(self.parent, setConstantWindow, 'edit_constant', event=event, parent_widget=self)

    # ----------------------------
    # Modify the selected stop
    def editStop(self, event=None):
        openWindow(self.parent, setStopWindow, 'edit_stop', event=event, parent_widget=self)

    # ---------------------
    # Modify the wait event
    def editWait(self, event=None):
        openWindow(self.parent, setWaitWindow, 'edit_wait', event=event, parent_widget=self)

    # ----------------------------------
    # Modify the experiment toggle event
    def editExperimentToggle(self, event=None):
        openWindow(self.parent, setExperimentToggleWindow, 'edit_exp_toggle', event=event, parent_widget=self)

    # -----------------------------
    # Move the event up in the list
    def moveEventUp(self, event_id=0):

        if event_id > 0:

            # Get the events
            crt_event = self.events[event_id]

            # Move the event up
            self.events[event_id-1], self.events[event_id] = self.events[event_id], self.events[event_id-1]

            # Reload the table
            self.fillEventTable()

    # -------------------------------
    # Move the event down in the list
    def moveEventDown(self, event_id=0):

        if event_id < len(self.events)-1:

            # Get the events
            crt_event = self.events[event_id]
            target_event = self.events[event_id+1]

            # Move the event down
            if target_event.event_type != 'Repeat':
                self.events[event_id+1], self.events[event_id] = self.events[event_id], self.events[event_id+1]

                # Reload the table
                self.fillEventTable()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ----------------------------
    # Save the scheduler in a file
    def saveInFile(self):

        # Check that the events aren't empty
        if self.events == []:
            errorMessage('No Events','There are no events in the scheduler. It cannot be saved to file.')
            return None

        # Prepare the default name
        default_name = os.path.join(self.parent.current_folder, 'scheduler.MCscd')

        # Select the file to save to
        fpath, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Scheduler as...", default_name, "Scheduler File (*.MCscd)")

        # Save the event in a file
        if fpath != "":
            schedulerToFile( fpath, self.events )

    # ----------------------------
    # Load a scheduler from a file
    def loadFromFile(self):

        # Search for the file to open
        fpath, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Open Scheduler File", self.parent.current_folder, "Scheduler File (*.MCscd);;All File (*.*)")

        # Read the file
        if fpath != "":
            file_content, pumps = fileToScheduler(fpath)

            # Assign the pumps
            lb = assignPumpWindow(pumps, parent=self.parent)
            lb.exec_()
            pump_dict = lb.GetValue()

            # Assign parents
            scheduler = []
            for event, pumps in file_content:

                # Assign the parents
                if isinstance(event, scd.ToggleExperiment) or isinstance(event, scd.RepeatScheduler):
                    event.parent = self.parent

                # Assign the pumps
                if len(pumps) > 0 and pump_dict is not None:
                    event.pumps = [pump_dict[x] for x in pumps]
                    event.getDescription()

                scheduler.append(event)

            # Assign the scheduler
            self.events = scheduler
            self.fillEventTable()

            # Notify the user
            if pump_dict is None:
                warningMessage('Scheduler Loaded', 'Scheduler has been loaded from file. Please check all the pumps assignment for EVERY event.')

    # ----------------------------------
    # Save the settings of the scheduler
    def saveScheduler(self):

        # Stop the current scheduler
        self.parent.stopScheduler()

        # Assign the new events
        self.parent.scheduler_elements = self.events

        # Generate the list of functions
        all_functions = []
        for event in self.events:
            crt_functions = event.getCommands()
            all_functions = all_functions + crt_functions
        self.parent.scheduler_functions = all_functions

        self.close()
        self.openScheduler()

    # -----------------------
    # Open the scheduler dock
    def openScheduler(self):

        # Open the dock
        _open_dock = True
        if "spectrum" in self.parent.docks.keys():
            if self.parent.docks["scheduler"] is not None:
                _open_dock = False

        if _open_dock:
            self.parent.docks["scheduler"] = SchedulerControllerPanel("Scheduler", self.parent)
            self.parent.addDockWidget(qtc.Qt.BottomDockWidgetArea, self.parent.docks["scheduler"])

            # Set the size and attach the dock
            self.parent.docks["scheduler"].setFloating(True)
            #self.parent.docks["spectrum"].detectLocationChange()
            #self.parent.docks["spectrum"].setFloating(False)
