import array
from threading import Thread, Event
from control_system.locomotive_controller import LocomotiveControlCore
from detection_system.detection_and_identification_system import DetectionHandler


class SystemCore:
    throttle_position: float = 0.0
    brake_position: float = 0.0

    speed_mph: float = 0.0
    speed_limit: float = 0.0

    threads: array = []

    event: Event

    locomotive_controller: LocomotiveControlCore = None
    detection_system: DetectionHandler = None

    def __init__(self, locomotive_controller: LocomotiveControlCore, detection_system: DetectionHandler):
        self.locomotive_controller = locomotive_controller
        self.detection_system = detection_system

        self.event = Event()

    def startup(self) -> bool:
        self.add_new_process_thread(Thread(target=self.detection_system.run, args=(self.event,), daemon=True))
        self.add_new_process_thread(Thread(target=self.locomotive_controller.run, args=(self.event,), daemon=True))

        self.locomotive_controller.connect()
        self.start_threads()

        return True

    def shutdown(self) -> bool:
        self.locomotive_controller.disconnect()
        self.stop_threads()

        self.threads = []

        return True

    def add_new_process_thread(self, thread):
        self.threads.append(thread)

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    def stop_threads(self):
        self.event.set()

        for thread in self.threads:
            thread.join()

        self.event.clear()
