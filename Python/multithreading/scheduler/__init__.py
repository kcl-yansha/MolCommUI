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

##-\-\-\-\-\-\
## TIMER CLASS
##-/-/-/-/-/-/

class schedulerTimer:

    def __init__ (self, scheduler, fn, *args, **kwargs):

        # Extract the value for the duration
        duration = kwargs.pop('duration', 10)
        if duration < 10:
            duration = 10

        # Define the timer
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(lambda: scheduler._run_scheduler(fn, *args, **kwargs))
        self.timer.setSingleShot(True)

        # Start the timer
        self.timer.start(duration)

    # ---------------
    # Abort the timer
    def close(self):

        # Stop all existing timers
        self.timer.stop()
        self.timer.deleteLater()

##-\-\-\-\-\-\-\-\
## SCHEDULER CLASS
##-/-/-/-/-/-/-/-/

class Scheduler:

    ##-\-\-\-\-\-\-\-\-\-\
    ## SCHEDULER MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------
    # (Re)set the settings and variables for the scheduler
    def resetScheduler(self):

        # Initialise the scheduler
        self.scheduler_running = False
        self.scheduler_elements = []
        self.scheduler_functions = []
        self.scheduler_id = -1
        self.scheduler_repeat = 0
        self.scheduler_variable = {}

    ##-\-\-\-\-\-\-\
    ## SCHEDULER RUN
    ##-/-/-/-/-/-/-/

    # ---------------------------
    # Start the scheduler session
    def startScheduler(self):

        if not self.scheduler_running and len(self.scheduler_functions) != 0:

            # Make sure nothing exists
            self.emptyScheduler()

            # Initialise the parameters
            self.scheduler_running = True
            self.scheduler_id = -1
            self.scheduler_repeat = 0

            # Start the scheduler
            if self.docks['scheduler'] is not None:
                self.docks['scheduler'].updateStatus(True)
            self._run_scheduler()

        elif self.scheduler_running:
            self.stopScheduler()

    # -------------------------------------
    # Run the next session of the scheduler
    def _run_scheduler(self, func=None, *args):

        # Interrupt if needed
        if not self.scheduler_running or self.scheduler_id >= len(self.scheduler_functions):
            self.stopScheduler()
            return 0

        # Run the function
        if func is not None:
            func(*args)

        # Update the iterator
        self.scheduler_id = self.scheduler_id + 1

        # Interrupt if needed
        if not self.scheduler_running or self.scheduler_id >= len(self.scheduler_functions):
            self.stopScheduler()
            return 0

        # Process the functions
        crt_cmd = self.scheduler_functions[self.scheduler_id]
        func = crt_cmd[0]
        duration = crt_cmd[1]
        note = crt_cmd[2]
        args = crt_cmd[3:]

        next_note = None
        if self.scheduler_id+1 < len(self.scheduler_functions):
            next_note = self.scheduler_functions[self.scheduler_id+1][2]

        # Run the function
        if note is not None and self.docks['scheduler'] is not None:
            self.docks['scheduler'].updateNote(note, next_note)

        #qtc.QTimer.singleShot(duration, lambda: self._run_scheduler(func, *args))
        self.scheduler_events.append( schedulerTimer(self, func, *args, duration=duration) )

    # --------------------------------------
    # Terminate the session of the scheduler
    def stopScheduler(self):

        self.scheduler_running = False
        self.emptyScheduler()

        # Notify the end of the run
        #winsound.Beep(440, 300)
        #winsound.Beep(494, 300)
        #winsound.Beep(554, 300)

        if self.docks['scheduler'] is not None:
            self.docks['scheduler'].updateStatus(False)
            self.docks['scheduler'].updateNote()

        try:
            self._end_scheduler()
        except:
            pass

    # -------------------
    # Empty the scheduler
    def emptyScheduler(self):

        # Check if it is possible to proceed
        try:
            len(self.scheduler_events)
        except:
            self.scheduler_events = []

        # Kill all instance of the timers
        for event in self.scheduler_events:
            try:
                event.close()
                self.scheduler_events.remove(event)
            except:
                pass
