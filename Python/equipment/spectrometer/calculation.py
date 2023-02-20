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

# ---------------------------------------------
# Get the integrated value over the given range
def _get_integration(x, y, w_ref, dw=2):

    # Get the mask
    value_mask = (x >= w_ref-dw) & (x <= w_ref+dw)

    # Extract the value
    selected_y = y[value_mask]

    # Sum the value
    integrated_y = np.sum(selected_y, axis=0)

    return integrated_y

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------
# Measure the absorbance
def getAbsorbance(intensity_measured, intensity_ref):

    # Calculate the intensity ratio
    if len(intensity_measured.shape) == 1:
        abs_spectrum = intensity_ref / intensity_measured
    else:
        abs_spectrum = intensity_ref[:,np.newaxis] / intensity_measured

    # Calculate the absorbance
    abs_spectrum = np.log10(abs_spectrum)

    return abs_spectrum

# ---------------------
# Rescale the intensity
def rescaleIntensity(x, y, y_ref, w_ref, dw=2):

    # Get the integrated intensities
    int_y = _get_integration(x, y, w_ref, dw=dw)
    int_ref = _get_integration(x, y_ref, w_ref, dw=dw)

    # Correct the intensity
    corr_factor = int_ref / int_y

    corrected_y = y * corr_factor

    return corrected_y
