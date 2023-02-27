import utils.settings_helper as settings_helper
import ctypes


class SimulatorAdapter:

    def connect(self) -> None:
        """Connect to the locomotive/simulator"""
        pass

    def is_connected(self) -> bool:
        """Test the application is connected to the locomotive"""

    def set_throttle(self, throttle_value=float) -> None:
        """Set the throttle value on the current locomotive"""
        pass

    def set_brake(self, brake_value=float) -> None:
        """Set the brake value of the current locomotive"""
        pass

    def apply_emergency_brake(self) -> bool:
        """Apply the emergency brake/full service brakes of the current locomotive"""
        pass

    def sound_horn(self) -> bool:
        """Sound the horn of the current locomotive"""
        pass

    def get_speed(self) -> float:
        """Get the speed of the current locomotive"""
        pass

    def get_brake(self) -> float:
        """Get the current brake application"""
        pass

    def get_throttle(self) -> float:
        """Get the current throttle position"""
        pass


class TrainSimClassicAdapter(SimulatorAdapter):
    dll = None
    connected = bool

    def __init__(self):
        dll_path = settings_helper.Settings().get_setting_value('DLL_PATH')
        self.dll = ctypes.cdll.LoadLibrary(dll_path)

    def connect(self) -> None:
        self.dll.SetRailDriverConnected(True)
        self.connected = True

    def is_connected(self) -> bool:
        return self.connected

    def set_throttle(self, throttle_value=float) -> None:
        self.dll.SetControllerValue('Throttle', ctypes.c_float(throttle_value))

    def set_brake(self, brake_value=float) -> None:
        self.dll.SetControllerValue('VirtualBrake', ctypes.c_float(brake_value))

    def apply_emergency_brake(self) -> bool:
        """Apply the emergency brake/full service brakes of the current locomotive"""
        pass

    def sound_horn(self) -> bool:
        """Sound the horn of the current locomotive"""
        pass

    def get_speed(self) -> float:
        return self.dll.GetControllerValue('SpeedometerMPH')

    def get_brake(self) -> float:
        return self.dll.GetControllerValue('VirtualBrake')

    def get_throttle(self) -> float:
        return self.dll.GetControllerValue('Throttle')
