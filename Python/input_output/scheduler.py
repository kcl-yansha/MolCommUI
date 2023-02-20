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

import multithreading.scheduler.events as scd

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------------------------------
# Get the wait event from the content dictionary
def _wait_from_dict(content):

    # Generate the event
    event = scd.Wait(
    float(content['duration'])
    )

    return event

# -----------------------------------------------
# Get the pulse event from the content dictionary
def _pulse_from_dict(content):

    # Generate the event
    event = scd.Pulse(
    [],
    int(content['npulses']),
    float(content['duration']),
    float(content['interval']),
    float(content['high']),
    float(content['low'])
    )

    return event

# ----------------------------------------------
# Get the stop event from the content dictionary
def _stop_from_dict(content):

    # Generate the event
    event = scd.Stop(
    [],
    float(content['duration'])
    )

    return event

# --------------------------------------------------
# Get the constant event from the content dictionary
def _constant_from_dict(content):

    # Generate the event
    event = scd.Constant(
    [],
    float(content['value']),
    float(content['duration'])
    )

    return event

# ------------------------------------------------
# Get the toggle event from the content dictionary
def _toggle_from_dict(content):

    # Get the values
    if content['status'] in ['true', 'yes', 'y', 't']:
        status = True
    else:
        status = False

    if content['new'] in ['true', 'yes', 'y', 't']:
        new = True
    else:
        new = False

    # Generate the event
    event = scd.ToggleExperiment(
    None,
    status,
    new
    )

    return event

# ------------------------------------------------
# Get the repeat event from the content dictionary
def _repeat_from_dict(content):

    # Generate the event
    event = scd.RepeatScheduler(
    None,
    int(content['max'])
    )

    return event

# ----------------------------------------
# Clean line from comments and empty lines
def _clean_line(line):

    if '#' in line:
        line, _ = line.split('#')
    elif '%' in line:
        line, _ = line.split('%')

    line = line.strip()

    return line

# -------------------------------------------------
# Convert the content of a string into a dictionary
def _content_do_dict(content):

    # Initialise
    parsed_content = {}

    # Parse all the elements
    for element in content.split(';'):
        key, value = element.split(':')
        parsed_content[key.strip().lower()] = value.strip().lower()

    return parsed_content

# -------------------------------------------
# Convert the line to the corresponding event
def _line_to_event(line):

    # Extract the list of pumps
    event_line = line.split('>>')

    # Check if pumps are detected
    if len(event_line)>1:

        # Extract the pumps
        event_pumps, event_line = event_line
        event_pumps = _pumps_from_content(event_pumps)

    else:
        event_line = event_line[0]
        event_pumps = []

    # Extract the line to ge the event type
    event_type, event_content = event_line.split('>')

    # Convert the input
    event_type = event_type.strip().lower()
    event_content = _content_do_dict(event_content)

    # Parse the line
    if event_type == 'wait':
        event = _wait_from_dict(event_content)
    elif event_type == 'pulse':
        event = _pulse_from_dict(event_content)
    elif event_type == 'stop':
        event = _stop_from_dict(event_content)
    elif event_type == 'constant':
        event = _constant_from_dict(event_content)
    elif event_type == 'toggleexp':
        event = _toggle_from_dict(event_content)
    elif event_type == 'repeatscd':
        event = _repeat_from_dict(event_content)
    else:
        event = None

    return event, event_pumps

# ----------------------------------------
# Extract the list of pumps from the input
def _pumps_from_content(content):

    # Get the list of pumps
    list_pumps = content.split(',')

    # Format the list
    if isinstance(list_pumps, list):
        list_pumps = [x.strip() for x in list_pumps]

    else:
        list_pumps = [list_pumps.strip()]

    return list_pumps

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------
# Load the scheduler from a file
def fileToScheduler(fpath):

    # Load the text from the file
    file_text = []
    with open(fpath, 'r') as scd_file:
        for line in scd_file:
            file_text.append(line)

    # Process all lines
    scheduler = []
    pumps = []
    for line in file_text:

        # Clean the line
        line = _clean_line(line)

        # Process the line
        if line != '':
            crt_event, crt_pumps = _line_to_event(line)

            for pump in crt_pumps:
                if pump not in pumps:
                    pumps.append(pump)

            if scheduler is not None:
                scheduler.append([crt_event, crt_pumps])

    return scheduler, pumps

# ----------------------------
# Save the scheduler in a file
def schedulerToFile(fpath,scheduler):

    # Initialise the text to write
    file_text = ''

    # Loop through all the events
    for event in scheduler:
        file_text += event.toString() + '\n'

    # Save the file
    with open(fpath, 'w') as scd_file:
        scd_file.write(file_text)
