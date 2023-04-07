import array
from enum import Enum
from threading import Event


class Thread:
    def run(self, event: Event):
        pass


class NotificationType(Enum):
    SPEED_MPH = 'SPEED_MPH'
    SPEED_LIMIT = 'SPEED_LIMIT'
    THROTTLE_POSITION = 'THROTTLE_POS'
    BRAKE_POSITION = 'BRAKE_POS'
    PREVIEW_IMAGE = 'PREVIEW_IMG'


class Publisher:
    subscribers: array = []

    def emit(self, notification_type: NotificationType, value):
        for observer in self.subscribers:
            observer.notify(notification_type, value)

    def register(self, *args):
        for item in args:
            self.subscribers.append(item)


class Subscriber:
    def notify(self, notification_type: NotificationType, value):
        pass
