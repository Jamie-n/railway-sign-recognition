import unittest
from control_system.locomotive_controller import TrainSimClassicAdapter, LocomotiveControlCore
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
