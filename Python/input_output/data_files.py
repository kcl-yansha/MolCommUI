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

import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------------------------
# Split the lines into two elements
def _split_line(text, split_at=':'):

    # Split the line
    line_content = text.strip().split(split_at)
    line_key = line_content[0]

    # Get the content
    if len(line_content) > 2:

        # Concatenate all elements
        line_value = line_content[1]
        for line in line_content[2]:
            line_value += line

        line_value = line_value.strip()
    else:
        line_value = line_content[1].strip()

    return line_key, line_value

# ------------------------------------
# Get the number of rows in the header
def _get_header_count(file_path):

    # Initialise the counter
    n_rows = 0
    get_type = True
    header_content = {'equipment_type':None}

    # Check the file
    with open(file_path, 'r') as file:
        for line in file:

            # Search for header
            if line[0] == '#':

                # Increment the counter
                n_rows += 1

                # Read the line
                crt_key, crt_value = _split_line(line[1:])

                # Get the equipment type
                if get_type:
                    header_content['equipment_type'] = crt_key
                    header_content['name'] = crt_value
                    get_type = False
                else:
                    header_content[crt_key] = crt_value

    return n_rows, header_content

# ---------------------------
# Get the name of the columns
def _get_column_names(file_path, n_rows):

    # Check the file
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):

            # Search for header
            if i == n_rows:
                column_names = line.strip().split(',')

    return column_names

# -----------------------------
# Convert data to step function
def _conv_2_step(data):

    # Split the data
    x, y = data[:,0], data[:,1]

    # Make new data
    x_step = [ x[0] ]
    y_step = [ y[0] ]

    for i, crt_x in enumerate( x[1:] ):

        # Append the previous point
        x_step.append(crt_x)
        y_step.append(y[i])

        # Append the current point
        x_step.append(crt_x)
        y_step.append(y[i+1])

    # Convert to array
    data_step = np.array( [x_step, y_step] ).T

    return data

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## EQUIPMENT-SPECIFIC FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# --------------------------
# Extract data for a syringe
def _extract_syringe(file_path, n_rows=4):

    # Extract the data
    data = np.loadtxt(file_path, skiprows=n_rows+1, delimiter=',', dtype=str)

    # Split the unit from the data
    unit = data[:,2]
    data = data[:,:2].astype(float)

    # UNIFY THE SPEED

    # Process the data
    data = _conv_2_step(data)

    return data

# ----------------------------
# Extract data for a flowmeter
def _extract_flowmeter(file_path, n_rows=4):

    # Extract the data
    data = np.loadtxt(file_path, skiprows=n_rows+1, delimiter=',')

    return data

# -------------------------------------------
# Extract the wavelength for the spectrometer
def _get_wavelength(column_names):

    # Get the wavelength
    wavelengths = []
    for wv in column_names[1:]:
        crt_wv, unit = wv.split(' ')

        wavelengths.append(float(crt_wv))

    # Format the output
    wavelengths = np.array(wavelengths)
    column_names = [
    column_names[0],
    'Wavelength ' + unit.strip()
    ]

    return column_names, wavelengths

# ------------------------------------
# Format the data for the spectrometer
def _format_spectrometer(data, wavelengths):

    # Split the data
    time, intensities = data[:,0], data[:,1:]

    # Build the array
    new_data = []
    for i, int_arr in enumerate(intensities):
        new_data.append( np.array([wavelengths, int_arr]).T )
    new_data = np.array(new_data)

    return [time, new_data]

# -------------------------------
# Extract data for a spectrometer
def _extract_spectrometer(file_path, column_names, n_rows=4):

    # Extract the data
    data = np.loadtxt(file_path, skiprows=n_rows+1, delimiter=',')

    # Get the wavelength
    column_names, wavelengths = _get_wavelength(column_names)

    # Format the data
    data = _format_spectrometer(data, wavelengths)

    return data, column_names

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------------------
# Check the type of equipment in the data file
def checkDataType(file_path):

    # Analyse the header
    _, header_content = _get_header_count(file_path)

    return header_content['equipment_type']

# ----------------
# Load a data file
def loadData(file_path):

    # Analyse the header
    n_rows, header_content = _get_header_count(file_path)

    # Get the name of the columns
    column_names = _get_column_names(file_path, n_rows)

    # Extract the data based on the equipment type
    if header_content['equipment_type'] == 'Syringe':
        data = _extract_syringe(file_path, n_rows=n_rows)

    if header_content['equipment_type'] == 'Flowmeter':
        data = _extract_flowmeter(file_path, n_rows=n_rows)

    if header_content['equipment_type'] == 'Spectrometer':
        data, column_names = _extract_spectrometer(file_path, column_names, n_rows=n_rows)

    return data, column_names, header_content
