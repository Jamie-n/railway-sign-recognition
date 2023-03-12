import time
from utils.helpers import PID
from control_system.control_system import TrainSimClassicAdapter


class LocomotiveControlCore:
    locomotive_controller: TrainSimClassicAdapter = None
    controller_core = None

    pid = None

    current_speed = 0.0
    speed_limit = 0.0

    throttle_position = 0.0
    brake_position = 0.0

    def __init__(self, controller: TrainSimClassicAdapter, controller_core):
        self.locomotive_controller = controller
        self.controller_core = controller_core
        self.pid = PID()

    def get_speed(self):
        return self.current_speed

    def connect(self):
        self.locomotive_controller.connect()

    def disconnect(self):
        self.locomotive_controller.disconnect()

    def update_current_speed(self):
        self.current_speed = self.locomotive_controller.get_speed()

    def control_speed(self, limit):
        self.speed_limit = limit
        self.update_current_speed()

        speed = int(limit) - int(self.current_speed)

        if speed > 0:
            self.set_brake(0)
            self.set_throttle(self.calculate_control_value())
        else:
            self.set_throttle(0)
            self.set_brake(abs(self.calculate_control_value()))

    def set_throttle(self, value: float):
        self.throttle_position = value
        self.locomotive_controller.set_throttle(value)

    def set_brake(self, value):
        print(value)
        self.brake_position = value
        self.locomotive_controller.set_brake(value)

    def get_throttle(self) -> float:
        return self.throttle_position

    def get_brake(self) -> float:
        return self.brake_position

    def calculate_control_value(self) -> float:
        return self.pid(int(self.speed_limit), int(self.current_speed)) / 100

