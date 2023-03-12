from __future__ import annotations

import time
from enum import Enum
import utils.settings_helper as settings_helper
import ctypes
from control_system.exceptions.control_exceptions import ControlOptionsNotLoadedException, SimulatorConnectionException


class ControlValues(Enum):
    SIMPLE_THROTTLE = 'SimpleThrottle'
    SIMPLE_CHANGE_DIRECTION = 'SimpleChangeDirection'
    REVERSER = 'Reverser'
    REGULATOR = 'Regulator'
    COMBINED_THROTTLE_AND_BRAKE = 'CombinedThrottleBrake'
    GEAR_LEVER = 'GearLever'
    TRAIN_BRAKE_CONTROL = 'TrainBrakeControl'
    ENGINE_BRAKE_CONTROL = 'EngineBrakeControl'
    DYNAMIC_BRAKE = 'DynamicBrake'
    EMERGENCY_BRAKE = 'EmergencyBrake'
    HAND_BRAKE = 'HandBrake'
    HORN = 'Horn'
    BELL = 'Bell'
    WIPERS = 'Wipers'
    SANDER = 'Sander'
    HEADLIGHTS = 'Headlights'
    AWS = 'AWS'
    AWS_RESET = 'AWSReset'
    AWS_CLEAR_COUNT = 'AWSClearCount'
    AWS_WARN_COUNT = 'AWSWarnCount'
    STARTUP = 'Startup'
    WHEELSLIP = 'Wheelslip'
    DOORS_OPEN_CLOSE_LEFT = 'DoorsOpenCloseLeft'
    DOORS_OPEN_CLOSE_RIGHT = 'DoorsOpenCloseRight'
    PANTOGRAPH_CONTROL = 'PantographControl'
    FRONT_PANTOGRAPH_CONTROL = 'FrontPantographControl'
    REAR_PANTOGRAPH_CONTROL = 'RearPantographControl'
    FIREBOX_DOOR = 'FireboxDoor'
    EXHAUST_INJECTOR_STEAM_ON_OFF = 'ExhaustInjectorSteamOnOff'
    EXHAUST_INJECTOR_WATER = 'ExhaustInjectorWater'
    LIVE_INJETOR_STEAM_ON_OFF = 'LiveInjectorSteamOnOff'
    LIVE_INJECTOR_WATER = 'LiveInjectorWater'
    DAMPER = 'Damper'
    BLOWER = 'Blower'
    STOKING = 'Stoking'
    CYLINDER_COCK = 'CylinderCock'
    STEAM_HEATING = 'SteamHeating'
    WATER_SCOOP_RAISE_LOWER = 'WaterScoopRaiseLower'
    SMALL_COMPRESSOR_ON_OFF = 'SmallCompressorOnOff'
    SPEEDOMETER_MPH = 'SpeedometerMPH'
    AMMETER = 'Ammeter'
    RPM_DIAL = 'RpmDial'
    ACCELEROMETER = 'Accelerometer'
    BRAKE_PIPE_PRESSURE_PSI = 'BrakePipePressurePSI'
    VACUUM_BRAKE_PIPE_PRESSURE_PSI = 'VacuumBrakePipePressurePSI'
    AIR_BRAKE_PIPE_PRESSURE_PSI = 'AirBrakePipePressurePSI'
    TRAIN_BRAKE_CYLINDER_PRESSURE_PSI = 'TrainBrakeCylinderPressurePSI'
    LOCO_BRAKE_CYLINDER_PRESSURE_PIS = 'LocoBrakeCylinderPressurePSI'
    MAIN_RESERVOIR_PRESSURE_PSI = 'MainReservoirPressurePSI'
    VACUUM_BRAKE_CHAMBER_PRESSURE_PSI = 'VacuumBrakeChamberPressurePSI'
    EQ_RESERVOIR_PRESSURE_PSI = 'EqReservoirPressurePSI'
    BRAKE_BAIL_OFF = 'BrakeBailOff'
    CURRENT = 'Current'
    TRACTIVE_EFFORT = 'TractiveEffort'
    RPM = 'RPM'
    RPM_DELTA = 'RPMDelta'
    COMPRESSOR_STATE = 'CompressorState'


class TrainSimClassicAdapter:
    dll = None
    connected = bool

    control_options = []

    def __init__(self):
        dll_path = settings_helper.Settings().get_setting_value('DLL_PATH')
        self.dll = ctypes.cdll.LoadLibrary(dll_path)

        self.dll.GetControllerList.restype = ctypes.c_char_p
        self.dll.GetControllerValue.restype = ctypes.c_float
        self.dll.SetRailDriverConnected.restype = ctypes.c_bool

    def connect(self) -> None:
        self.connected = self.dll.SetRailDriverConnected(True)
        self.load_control_options()

        return self.connected

    def disconnect(self):
        self.connected = self.dll.SetRailDriverConnected(False)
        self.connected = False

    """
    Test the application is connected to the simulator before attempting to operate upon the dll 
    """

    def check_connection(self) -> bool | SimulatorConnectionException:
        if not self.connected:
            raise SimulatorConnectionException

        return True

    """
    Get all the control options for the selected locomotive
    """

    def get_control_options(self):
        return self.dll.GetControllerList().decode().split('::')

    def load_control_options(self):
        self.check_connection()

        self.control_options = self.get_control_options()

    def control_option_to_index(self, option_name: str):
        if not len(self.control_options):
            raise ControlOptionsNotLoadedException

        try:
            return self.control_options.index(option_name)
        except:
            return False

    def set_control_value(self, control_option: ControlValues, value):
        control_index = self.control_option_to_index(str(control_option.value))

        if control_index:
            self.dll.SetControllerValue(control_index, ctypes.c_float(value))

    def get_control_value(self, control_option: ControlValues):
        control_index = self.control_option_to_index(str(control_option.value))

        if control_index:
            return self.dll.GetControllerValue(control_index, 0)

        return False

    """Sound the horn of the current locomotive"""
    def sound_horn(self, value: int) -> None:
        self.set_control_value(ControlValues.HORN, True)
        time.sleep(0.5)
        self.set_control_value(ControlValues.HORN, False)

    def get_speed(self) -> float:
        return self.get_control_value(ControlValues.SPEEDOMETER_MPH)

    def set_throttle(self, value: float):
        self.set_control_value(ControlValues.REGULATOR, value)

    def set_brake(self, value: float):
        self.set_control_value(ControlValues.TRAIN_BRAKE_CONTROL, value)
