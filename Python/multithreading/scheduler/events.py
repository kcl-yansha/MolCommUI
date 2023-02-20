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

# ------------------------------------
# Get the string for the list of pumps
def _get_pump_list(event):

    if len(event.pumps) > 0:

        pump_desc = str(event.pumps[0].name)
        for p in event.pumps[1:]:
            pump_desc += ', ' + str(p.name)

    else:
        pump_desc = ''

    return pump_desc

##-\-\-\-\-\
## FUNCTIONS
##-/-/-/-/-/

# ------------------------------------
# Edit the value of the selected pumps
def setPumpEvent(pumps, flowrate):

    for pump in pumps:

        if flowrate != 0:

            # Change the speed of the pump
            pump.equipment.editSetSpeed(flowrate)
            pump.setSpeed(priority=True)

            # Run the pump
            pump.run()

        else:

            # Stop the pump
            pump.stop()

# ---------
# Just wait
def setWaitEvent():
    pass # Do absolutely nothing

# -----------------------------------------------
# Copy the existing experiment to start a new one
def toggleExperiment(parent, status):
    parent.toggleRecording(status)

# -----------------------------------------------
# Copy the existing experiment to start a new one
def copyExperiment(parent):
    parent.duplicateExperiment()

# --------------------
# Repeat the scheduler
def repeatScheduler(parent, max_repeat):

    if parent.scheduler_repeat < max_repeat:

        # Restart the scheduler
        parent.scheduler_id = -1

        # Move the incrementation
        parent.scheduler_repeat += 1

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## SET & EDIT VARIABLE CLASS
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class SetVariable:
    def __init__(self, name, value):

        self.event_type = 'SetVar'

        # Set the general parameters
        self.name = name
        self.value = value
        self.pumps = []

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):
        self.description = 'Set Var. ' + str(self.name) + ' = ' + str(self.value)
        self.pump_desc = ''

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Re-initialise
        self.commands = []

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):
        return 'SetVar > Name:' + str(self.name) + ' ; Value:"' + str(self.value) + '"'

##-\-\-\-\-\
## WAIT CLASS
##-/-/-/-/-/

class Wait:
    def __init__(self, duration):

        self.event_type = 'Wait'

        # Set the general parameters
        self.duration = duration
        self.pumps = []

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):

        self.description = 'Wait ' + str(self.duration) + ' min'
        self.pump_desc = ''

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Re-initialise
        self.commands = [(setWaitEvent, self.duration * 60 * 1000, 'Wait for '+str(self.duration))]

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):
        return 'Wait > Duration:' + str(self.duration)

##-\-\-\-\-\-\
## PULSE CLASS
##-/-/-/-/-/-/

class Pulse:
    def __init__(self, pumps, n_pulses, duration, interval, high, low=0):

        self.event_type = 'Pulse'

        # Assign the pumps
        self.pumps = pumps

        # Set the general parameters
        self.n_pulses = n_pulses
        self.duration = duration
        self.interval = interval
        self.high = high
        self.low = low

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):

        #
        self.description = str(self.n_pulses) + ' Pulses ' + str(self.high) + '/'+str(self.low) + ' uL/min'
        self.description += ' d:'+str(self.duration)+ ',i:'+str(self.interval)+' min'

        self.pump_desc = _get_pump_list(self)

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Re-initialise
        self.commands = []

        # Add all the pulses
        for i in range(self.n_pulses):

            # Make one pulse + trailer
            self.commands.append( (setPumpEvent, 0, None, self.pumps, self.high) )
            self.commands.append( (setPumpEvent, self.duration * 60 * 1000, 'Set Pulse on', self.pumps, self.low) )
            self.commands.append( (setPumpEvent, self.interval * 60 * 1000, 'Set Pulse off', self.pumps, self.low) )

        # Remove the last interval
        self.commands.pop()

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):

        # Generate the text
        output_text = self.pump_desc + ' >> Pulse > NPulses:' + str(self.n_pulses)
        output_text +=  '; Duration:' + str(self.duration)
        output_text +=  '; Interval:' + str(self.interval)
        output_text +=  '; High:' + str(self.high)
        output_text +=  '; Low:' + str(self.low)

        return output_text

##-\-\-\-\-\
## STOP CLASS
##-/-/-/-/-/

class Stop:
    def __init__(self, pumps, duration=0):

        self.event_type = 'Stop'

        # Assign the pumps
        self.pumps = pumps

        # Set the general parameters
        self.duration = duration

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):

        self.description = 'Stop'
        if self.duration != 0:
            self.description += ' d:'+str(self.duration)+ ' min'

        self.pump_desc = _get_pump_list(self)

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Re-initialise
        self.commands = []

        # Add all the pulses
        if self.duration != 0:
            self.commands.append( (setPumpEvent, 0, None, self.pumps, 0) )
            self.commands.append( (setPumpEvent, self.duration * 60 * 1000, 'Stop pumps', self.pumps, 0) )

        else:
            self.commands.append( (setPumpEvent, 0, 'Stop pumps', self.pumps, 0) )

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):
        return self.pump_desc + ' >> Stop > Duration:' + str(self.duration)

##-\-\-\-\-\-\-\
## CONSTANT CLASS
##-/-/-/-/-/-/-/

class Constant:
    def __init__(self, pumps, value, duration=0):

        self.event_type = 'Constant'

        # Assign the pumps
        self.pumps = pumps

        # Set the general parameters
        self.duration = duration
        self.value = value

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):

        self.description = 'Cst ' + str(self.value) + ' uL/min'
        if self.duration != 0:
            self.description += ' d:'+str(self.duration)+ ' min'

        self.pump_desc = _get_pump_list(self)

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Re-initialise
        self.commands = []

        # Add all the pulses
        if self.duration != 0:
            self.commands.append( (setPumpEvent, 0, None, self.pumps, self.value) )
            self.commands.append( (setPumpEvent, self.duration * 60 * 1000, 'Set constant to '+str(self.value), self.pumps, self.value) )

        else:
            self.commands.append( (setPumpEvent, 0, 'Set constant to '+str(self.value), self.pumps, self.value) )

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):
        return self.pump_desc + ' >> Constant > Value:' + str(self.value) + '; Duration:' + str(self.duration)

##-\-\-\-\-\-\-\-\-\-\-\-\
## TOGGLE EXPERIMENT CLASS
##-/-/-/-/-/-/-/-/-/-/-/-/

class ToggleExperiment:
    def __init__(self, parent, status, new):

        self.event_type = 'ToggleExp'

        # Set the general parameters
        self.parent = parent
        self.status = status
        self.new = new

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):

        self.description = 'Toggle Exp. ' + str(self.status)
        if self.new:
            self.description += ' (New)'

        self.pump_desc = ''

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Re-initialise
        self.commands = []

        # Assemble the commands
        if self.new and self.status:
            self.commands.append( (copyExperiment, 0, 'New experiment', self.parent) )

        self.commands.append( (toggleExperiment, 0, 'Set experiment '+str(self.status), self.parent, self.status) )

        if self.new and not self.status:
            self.commands.append( (copyExperiment, 0, 'New experiment', self.parent) )

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):
        return 'ToggleExp > Status:' + str(self.status) + ' ; New:' + str(self.new)

##-\-\-\-\-\-\-\-\-\-\-\
## REPEAT SCHEDULER CLASS
##-/-/-/-/-/-/-/-/-/-/-/

class RepeatScheduler:
    def __init__(self, parent, max_repeat):

        self.event_type = 'Repeat'

        # Set the general parameters
        self.parent = parent
        self.max_repeat = max_repeat

        # Inialise the list of commands
        self.getCommands()
        self.getDescription()

    ##-\-\-\
    ## EVENTS
    ##-/-/-/

    # --------------------------------
    # Get the description of the event
    def getDescription(self):

        self.description = 'Repeat ' + str(self.max_repeat)

        self.pump_desc = ''

    # ------------------------
    # Get the list of commands
    def getCommands(self):

        # Set the commands
        self.commands = [(repeatScheduler, 0, 'Restart scheduler', self.parent, self.max_repeat)]

        return self.commands

    ##-\-\-\-\
    ## FILE I/O
    ##-/-/-/-/

    # --------------------------------------------------------------
    # Convert the content of the class into a string to save in file
    def toString(self):
        return 'RepeatScd > Max:' + str(self.max_repeat)
