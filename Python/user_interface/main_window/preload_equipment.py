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

from equipment.connection.arduino import get_list_ports
from equipment.flow_meter.equipment_class import loadFlowMeterClass
from equipment.spectrometer.commands import get_list_spectrometers
from equipment.spectrometer.equipment_class import loadSpectroMeterClass
from equipment.syringe_pump.equipment_class import SyringeEquipment, loadSyringeGroupClass
from settings.equipment.reload_equipment import getEquipmentList, getPortInfos

from user_interface.popups.notifications import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\-\
## MAIN GUI OF THE SOFTWARE
##-/-/-/-/-/-/-/-/-/-/-/-/

class mainGUIPreloadFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\
    ## SETTINGS MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------
    # Pre-load the equipment
    def preloadEquipment(self):

        # Check the user config
        is_enabled, equipment_list = getEquipmentList( user_name=self.main_config['current_user'] )

        # Try to load the equipment
        try:

            # Load the equipment
            if is_enabled and len(equipment_list) > 0:

                # Loop over all the equipment
                for equipment in equipment_list:

                    # Check that the port is connected
                    if (equipment in get_list_ports() or equipment in get_list_spectrometers()) and equipment not in self.active_ports:

                        # Load the dictionary
                        equipment_dict = getPortInfos( equipment, user_name=self.main_config['current_user'] )

                        # Load the appropriate equipment
                        if equipment_dict['equipment_type'] == 'flowmeter':
                            self.loadFlowmeter( equipment, equipment_dict )

                        elif equipment_dict['equipment_type'] == 'syringe_pump':
                            self.loadSyringePumps( equipment, equipment_dict )

                        elif equipment_dict['equipment_type'] == 'spectrometer':
                            self.loadSpectrometer( equipment, equipment_dict )

        except:
            pass

    ##-\-\-\-\-\-\-\-\-\
    ## LOAD THE EQUIPMENT
    ##-/-/-/-/-/-/-/-/-/

    # ------------------
    # Load the flowmeter
    def loadFlowmeter(self, port, equipment_dict):

        # Try opening the port
        opened_meter = loadFlowMeterClass(self, port)

        # Raise an error if connection fail
        if opened_meter is None:
            errorMessage("Flow meter preload fail", "No Flow meter was detected at the saved port ("+port+").")
            return 0

        # Proceed to load the flowmeter
        self.active_ports.append(port)
        opened_meter.name = equipment_dict['name']
        opened_meter.ftype = equipment_dict['ftype']
        opened_meter.pid_controller = equipment_dict['pid']
        opened_meter.use_previous = equipment_dict['filter-use'] == 'True'
        opened_meter.n_previous = int( equipment_dict['filter-wsize'] )

        # Set the different settings
        opened_meter.updatePIDType()

        # Initialise the flowmeter
        opened_meter.init(equipment_dict['ftype'])

        # Refresh the information for the files
        opened_meter.getFileInfos()

        # Add the flow meter to the connected elements
        self.equipments['flow_meter'].append(opened_meter)

        # Update the main window
        self.groupDisplay.addFlowMeter( opened_meter )

    # ---------------------
    # Load the spectrometer
    def loadSpectrometer(self, port, equipment_dict):

        # Try opening the port
        opened_meter = loadSpectroMeterClass(self, port)

        # Raise an error if connection fail
        if opened_meter is None:
            errorMessage("Spectrometer preload fail", "No Spectrometer was detected at the saved port ("+port+").")
            return 0

        # Proceed to load the flowmeter
        self.active_ports.append(port)
        opened_meter.name = equipment_dict['name']
        opened_meter.setIntegrationTime( int(equipment_dict['integration']) )
        opened_meter.delay_time = int(equipment_dict['delay'])

        # Add the flow meter to the connected elements
        self.equipments['spectrometer'].append(opened_meter)

        # Update the main window
        self.groupDisplay.addSpectroMeter( opened_meter )

    # ---------------------
    # Load the syringe pump
    def loadSyringePumps(self, port, equipment_dict):

        # Try opening the port
        opened_group = loadSyringeGroupClass(self, port)

        # Raise an error if connection fail
        if opened_group is None:
            errorMessage("Syringe pump preload fail", "No Syringe pump was detected at the saved port ("+port+").")
            return 0

        # Proceed to load the flowmeter
        self.active_ports.append(port)
        opened_group.name = equipment_dict['name']

        # Load the individual syringes
        loaded_axis = []
        for key_name in equipment_dict.keys():

            # Get the axis
            if '_name' in key_name:
                axis, _ = key_name.split('_')
                loaded_axis.append(axis.upper())

                # Get the class
                crt_syringe = SyringeEquipment(opened_group, axis_port=axis.upper(), debug=self.main_config['debug_syringe_send'], verbose=self.main_config['debug_syringe'])
                crt_syringe.name = equipment_dict[key_name]
                crt_syringe.equipment.stype = equipment_dict[axis+'_type']
                crt_syringe.equipment.geartype = equipment_dict[ axis+'_gear' ]
                crt_syringe.equipment.unit = equipment_dict[axis+'_unit']
                crt_syringe.equipment.speed = float(equipment_dict[axis+'_speed'])
                crt_syringe.equipment.acceleration = float(equipment_dict[axis+'_accel'])

                # Save the class
                self.equipments['syringe_pumps'].append( crt_syringe )

                # Set the different settings
                crt_syringe.equipment.updateSyringeType()
                crt_syringe.equipment.updateGearboxType()

                # Save the value
                crt_syringe.equipment.editSetSpeed( float(equipment_dict[axis+'_speed']) )

                crt_syringe.setSpeed()
                crt_syringe.setAccel()

                # Update the main window
                self.groupDisplay.addSyringe( crt_syringe )

        # Empty unwanted axis
        for axis in opened_group.syringes.keys():
            if axis not in loaded_axis:
                opened_group.syringes[axis] = None
                opened_group.syringe_equipments[axis] = None
