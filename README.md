# MolCommUI
 
## General Information

### About MolCommUI...
- **Version:** 1.0
- **Release date:** 20/02/2023

MolCommUI is a Python3 software running with the GUI framework PyQt5, allowing to control platforms designed for typical Molecular Communication applications.
MolCommUI integrates the following functions
- Timed and scheduled chemical injection (e.g., using syringe pumps)
- Flow rate measurement and control via PID controller
- UV-Visible spectrometry measurement

The software is designed so the platform is fully automated

### Authors and contributions
The Python code was made by
- Vivien WALTER (vivien.walter@kcl.ac.uk, [GitHub](https://github.com/vivien-walter), [Website](https://vivien-walter.github.io))

The Arduino code was adapted from the source code of the [Poseidon pumps](https://pachterlab.github.io/poseidon/) from the Patcher lab, corrected and revised by
- Dadi BI (dadi.bi@kcl.ac.uk)
- Vivien WALTER

The research project which lead to the creation of MolCommUI was supervised by 
- Yansha DENG (yansha.deng@kcl.ac.uk, [Website](https://www.yanshadeng.org))

## How-to install

### Requirements

#### Python
To operate MolCommUI, the following Python module are required on your computer.
- PyQt5
- NumPy
- pyqtgraph
- appdirs
- pyserial
- seabreeze

#### Arduino
The only package you will need to install to run the Arduino code from this repo is
- AccelStepper.h

You can install this package directly from the **Library Manager** of the Arduino IDE.

### Step-by-step guide
This guide has been tested on **MacOS**, **Ubuntu**, and **Windows** (using Windows Terminal and Powershell).

#### MolCommUI (Python GUI software)

1. Download the code from GitHub and copy the Python folder on your computer
2. Open the **Terminal** inside the Python folder
3. (Optional) Create a virtual environment for operating the Python code
4. Install all the required python module. This can be done by using the *requirements.txt* file from the GitHub repo and the command 
`pip install -r requirements.txt`
5. Start the software by typing the command
`python main.py`
If you are running the software on Ubuntu, you might have to run the command above as `sudo`.

#### Stepper\_Controller (Arduino code for the syringe pumps)
In order to use the Stepper\_Controller code on your Arduino, you will first need to mount a CNC shield and make the appropriate connection and wiring. You can find all the instructions at [this link](https://pachterlab.github.io/poseidon/hardware).

You will then need to install the version of the Arduino code from our GitHub repo
1. Download the code from GitHub and copy the Arduino folder on your computer
2. Connect the Arduino to your computer
3. Open the **Arduino IDE**, make sure *AccelStepper.h* is installed and that the correct port is selected for your Arduino board
4. Open the file **Stepper\_Controller.ino** into the Arduino IDE
5. (Optional) Change the value of the variable *DEVICEID* if you use multiple pumps to identify them.
6. Upload the code on the Arduino board.

## Compatible equipment
This section list all the equipment which have been successfully tested on our software

### Pumps
So far, the software has only be tested with home-made 3D printed syringe pumps based on stepper motors controlled by Arduino (see [Poseidon pumps](https://pachterlab.github.io/poseidon/)).

For commercial pumps, modification of the source code of MolCommUI might be necessary.

### Flow meter
The software was successfully tested with the following flow meter(s):
- Sensirion SLI-0430
- Sensirion SLF3S-0600F

For support of other flow meters from Sensirion, please [contact the company](https://sensirion.com) for assistance with their API.
For flow meters from other makers, modification of the source code of MolCommUI might be necessary.

### Spectrometer
The software was successfully tested with the following spectrometer(s):
- Ocean Insight Flame-UV-Vis spectrometer

For support of other flow meters from Ocean Insight, we recommend checking the page of the [seabreeze Python module](https://github.com/ap--/python-seabreeze).

## Citations
*To be added*