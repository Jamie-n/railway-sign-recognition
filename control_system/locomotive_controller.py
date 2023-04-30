import array
import time
from interfaces import Thread, Publisher, NotificationType, Subscriber
from utils.helpers import PID
from control_system.control_system import TrainSimClassicAdapter


class LocomotiveControlCore(Thread, Publisher, Subscriber):
    locomotive_controller: TrainSimClassicAdapter = None
    pid = None

    throttle_position = 0.0
    brake_position = 0.0

    speed_limit: int = 0

    def __init__(self, controller: TrainSimClassicAdapter):
        self.locomotive_controller = controller
        self.pid = PID()

    def notify(self, notification_type: NotificationType, value):
        if notification_type == NotificationType.SPEED_LIMIT:
            self.speed_limit = int(value)

    def run(self, event) -> None:
        while not event.isSet():
            self.manage_speed()
            time.sleep(0.1)

        self.set_brake(0)
        self.set_throttle(0)
        self.emit(NotificationType.SPEED_MPH, 0)


    def manage_speed(self):
        self.emit(NotificationType.SPEED_MPH, self.get_speed())

        if self.speed_difference() > 0:
            self.set_brake(0)
            self.set_throttle(self.calculate_control_value())
        else:
            self.set_throttle(0)
            self.set_brake(abs(self.calculate_control_value()))

    def speed_difference(self):
        return self.speed_limit - self.get_speed()

    def get_speed(self):
        return self.locomotive_controller.get_speed()

    def connect(self):
        return self.locomotive_controller.connect()

    def disconnect(self):
        self.locomotive_controller.disconnect()

    def set_throttle(self, value: float):
        self.throttle_position = value
        self.locomotive_controller.set_throttle(value)
        self.emit(NotificationType.THROTTLE_POSITION, value)

    def set_brake(self, value):
        self.brake_position = value
        self.locomotive_controller.set_brake(value)
        self.emit(NotificationType.BRAKE_POSITION, value)

    def get_throttle(self) -> float:
        return self.throttle_position

    def get_brake(self) -> float:
        return self.brake_position

    def calculate_control_value(self) -> float:
        return self.pid(int(self.speed_limit), int(self.locomotive_controller.get_speed())) / 100
