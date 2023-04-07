import unittest
from control_system.locomotive_controller import LocomotiveControlCore, TrainSimClassicAdapter
import numpy as np
from control_system.control_system import ControlValues
from control_system.exceptions.control_exceptions import SimulatorConnectionException, ControlOptionsNotLoadedException
from unittest.mock import MagicMock


class TestLocomotiveControl(unittest.TestCase):

    def test_sets_brake_zero_when_accelerating(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.get_speed = MagicMock(return_value=51.89)
        ts_classic_adapter.set_throttle = MagicMock()
        ts_classic_adapter.set_brake = MagicMock()
        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.brake_position = 0.89
        control_core.speed_limit = 65

        self.assertEqual(control_core.brake_position, 0.89)

        control_core.manage_speed()

        self.assertEqual(control_core.brake_position, 0)

    def test_sets_throttle_when_acceleration_is_required(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.get_speed = MagicMock(return_value=25.04)
        ts_classic_adapter.set_throttle = MagicMock()
        ts_classic_adapter.set_brake = MagicMock()
        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.speed_limit = 40

        control_core.manage_speed()

        self.assertGreater(control_core.throttle_position, 0)

    def test_sets_throttle_zero_when_braking(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.get_speed = MagicMock(return_value=51.89)
        ts_classic_adapter.set_throttle = MagicMock()
        ts_classic_adapter.set_brake = MagicMock()
        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.throttle_position = 0.45
        control_core.speed_limit = 40

        self.assertEqual(control_core.throttle_position, 0.45)

        control_core.manage_speed()

        self.assertEqual(control_core.throttle_position, 0)

    def test_sets_brake_when_braking_required(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.get_speed = MagicMock(return_value=51.89)
        ts_classic_adapter.set_throttle = MagicMock()
        ts_classic_adapter.set_brake = MagicMock()
        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.speed_limit = 40

        control_core.manage_speed()

        self.assertGreater(control_core.brake_position, 0)

    def test_brake_position_recorded_when_set(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.set_brake = MagicMock()

        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.set_brake(45)

        self.assertEqual(45, control_core.brake_position)

    def test_throttle_position_recorded_when_set(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.set_throttle = MagicMock()

        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.set_throttle(8)

        self.assertEqual(8, control_core.throttle_position)

    def can_calculate_control_value(self):
        pass

    def test_can_handle_negative_speed_limit(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.get_speed = MagicMock(return_value=90)
        ts_classic_adapter.set_throttle = MagicMock()
        ts_classic_adapter.set_brake = MagicMock()
        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.brake_position = 0.89
        control_core.speed_limit = -15

        control_value = control_core.calculate_control_value()

        self.assertEqual(-5.83275, control_value)

    def test_can_handle_large_speed_difference_when_calculating_control_value(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.get_speed = MagicMock(return_value=1)
        ts_classic_adapter.set_throttle = MagicMock()
        ts_classic_adapter.set_brake = MagicMock()
        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.brake_position = 0.89
        control_core.speed_limit = 9999

        control_value = control_core.calculate_control_value()

        self.assertEqual(555.3889, control_value)

    def can_apply_braking(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.set_brake = MagicMock()

        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.set_throttle(0.315)

        ts_classic_adapter.set_brake().assert_called_with(0.315)

    def test_can_set_throttle(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.set_throttle = MagicMock()

        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.set_throttle(10.015)

        ts_classic_adapter.set_throttle.assert_called_with(10.015)

    def test_can_disconnect_from_adapter(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.disconnect = MagicMock(return_value=True)

        control_core = LocomotiveControlCore(ts_classic_adapter)

        control_core.disconnect()

        ts_classic_adapter.disconnect.assert_called()

    def test_can_connect_to_adapter(self):
        ts_classic_adapter = TrainSimClassicAdapter
        ts_classic_adapter.connect = MagicMock(return_value=True)

        control_core = LocomotiveControlCore(ts_classic_adapter)

        self.assertTrue(control_core.connect())

        ts_classic_adapter.connect.assert_called()

class TestTrainSimClassicAdapter(unittest.TestCase):
    mocked_train_sim_classic_adapter = None

    def setUp(self) -> None:
        self.mocked_train_sim_classic_adapter = TrainSimClassicAdapter
        self.mocked_train_sim_classic_adapter.__init__ = MagicMock(return_value=None)
        self.mocked_train_sim_classic_adapter.dll = DLLMock()

    def test_can_connect(self):
        self.assertTrue(TrainSimClassicAdapter().connect())

    def test_can_disconnect(self):
        adapter = TrainSimClassicAdapter()

        adapter.connect()

        self.assertTrue(adapter.connected)

        adapter.disconnect()

        self.assertFalse(adapter.connected)

    def test_can_handle_disconnected_when_not_connected(self):
        adapter = TrainSimClassicAdapter()

        adapter.disconnect()

        self.assertFalse(adapter.connected)

    def test_check_connection_returns_true_when_connected(self):
        adapter = TrainSimClassicAdapter()

        adapter.connect()

        self.assertTrue(adapter.connected)

        self.assertTrue(adapter.check_connection())

    def test_check_connection_raised_exception_when_not_connected(self):
        adapter = TrainSimClassicAdapter()

        adapter.connect()

        self.assertTrue(adapter.connected)

        adapter.disconnect()

        self.assertFalse(adapter.connected)

        with self.assertRaises(SimulatorConnectionException):
            adapter.check_connection()

    def test_can_load_control_options_from_dll(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()

        self.assertEqual(
            ['Active', 'TractiveEffort', 'EngineStart', 'Startup', 'RPM', 'RPMDelta', 'Ammeter',
             'VacuumBrakeChamberPressureINCHES', 'VacuumBrakePipePressureINCHES', 'AirBrakePipePressureBAR',
             'LocoBrakeCylinderPressurePSI', 'LocoBrakeCylinderPressurePSI', 'MainReservoirPressurePSI',
             'SpeedometerMPH', 'CompressorState', 'Reverser', 'SimpleChangeDirection', 'Regulator', 'SimpleThrottle',
             'EngineBrakeControl', 'TrainBrakeControl', 'HandBrake', 'EmergencyBrake', 'Horn', 'Headlights', 'Sander',
             'Wipers', 'AWS', 'AWSReset', 'AWSClearCount', 'AWSWarnCount', 'DoorsOpenClose', 'GlarePanels', 'CabLight',
             'InstrumentLights', 'DestinationK', 'DestinationH', 'DestinationT', 'DestinationU'],
            adapter.get_control_options())

    def test_throws_exception_when_attempting_to_load_control_options_when_not_connected(self):
        adapter = TrainSimClassicAdapter()
        adapter.disconnect()

        self.assertFalse(adapter.connected)

        with self.assertRaises(SimulatorConnectionException):
            adapter.load_control_options()

    def test_can_convert_control_option_string_to_index(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()

        self.assertEqual(6, adapter.control_option_to_index(ControlValues.AMMETER.value))

    def test_throws_control_options_not_loaded_if_control_options_are_empty(self):
        adapter = TrainSimClassicAdapter()

        with self.assertRaises(ControlOptionsNotLoadedException):
            adapter.control_option_to_index(ControlValues.AMMETER.value)

    def test_can_handle_invalid_control_option_conversion(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()

        self.assertFalse(adapter.control_option_to_index('invalid_value'))

    def test_can_set_control_value(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()

        adapter.set_control_value(ControlValues.SIMPLE_THROTTLE, 0.52)

        self.assertEqual(str(np.float32(adapter.dll.controls[18])), '0.52')

    def test_can_get_control_value(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()

        adapter.set_control_value(ControlValues.SIMPLE_THROTTLE, 0.52)
        adapter.set_control_value(ControlValues.TRAIN_BRAKE_CONTROL, 0)

        self.assertEqual('0.0', str(np.float32(adapter.get_control_value(ControlValues.TRAIN_BRAKE_CONTROL))))

    def test_can_get_speed(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()

        adapter.set_control_value(ControlValues.SPEEDOMETER_MPH, 28.48)

        self.assertEqual('28.48', str(np.float32(adapter.get_speed())))

    def test_can_set_throttle(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()
        adapter.set_throttle(0.49)

        self.assertEqual('0.49', str(np.float32(adapter.get_throttle())))

    def test_can_set_brake(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()
        adapter.set_brake(0.36)

        self.assertEqual('0.36', str(np.float32(adapter.get_brake())))

    def test_can_get_brake(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()
        adapter.set_control_value(ControlValues.TRAIN_BRAKE_CONTROL, 0.16)

        self.assertEqual('0.16', str(np.float32(adapter.get_brake())))

    def test_can_get_throttle(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()
        adapter.set_control_value(ControlValues.REGULATOR, 0.94)

        self.assertEqual('0.94', str(np.float32(adapter.get_throttle())))

    def test_can_sound_horn(self):
        adapter = TrainSimClassicAdapter()
        adapter.connect()
        adapter.sound_horn(True)

        self.assertTrue(adapter.get_control_value(ControlValues.HORN))


class DLLMock:
    controls = {}

    def SetRailDriverConnected(self, connected) -> bool:
        return connected

    def GetControllerList(self):
        return 'Active::TractiveEffort::EngineStart::Startup::RPM::RPMDelta::Ammeter::VacuumBrakeChamberPressureINCHES::VacuumBrakePipePressureINCHES::AirBrakePipePressureBAR::LocoBrakeCylinderPressurePSI::LocoBrakeCylinderPressurePSI::MainReservoirPressurePSI::SpeedometerMPH::CompressorState::Reverser::SimpleChangeDirection::Regulator::SimpleThrottle::EngineBrakeControl::TrainBrakeControl::HandBrake::EmergencyBrake::Horn::Headlights::Sander::Wipers::AWS::AWSReset::AWSClearCount::AWSWarnCount::DoorsOpenClose::GlarePanels::CabLight::InstrumentLights::DestinationK::DestinationH::DestinationT::DestinationU'.encode()

    def SetControllerValue(self, control_index, value):
        self.controls.update({control_index: value})

    def GetControllerValue(self, control_index, foo):
        return self.controls[control_index]
