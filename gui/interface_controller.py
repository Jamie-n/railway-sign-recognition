import threading
from threading import Event
from kivy.properties import partial
from kivy.clock import mainthread, Clock
from kivymd.app import MDApp
from kivy.base import Builder
from kivy.uix.widget import Widget
from gui.settings_controller import SettingsMenuContent
from kivy.core.window import Window
import utils.helpers as helpers
from detection_system.detection_and_identification_system import DetectionHandler
from control_system.locomotive_controller import LocomotiveController


class InterfaceController(Widget):
    event = Event()
    thread = None

    current_speed = 00
    current_limit = 00
    current_throttle = 00
    current_brake = 00

    def open_settings(self):
        SettingsMenuContent().show_settings()

    def begin_detection(self):
        self.ids.stop_detection_button.disabled = False
        self.ids.start_detection_button.disabled = True

        self.thread = threading.Thread(target=self.run_speed_detection, args=(self.event,), daemon=True)

        self.thread.start()

    def halt_detection(self):
        self.ids.start_detection_button.disabled = False
        self.ids.stop_detection_button.disabled = True

        self.event.set()

        self.thread.join()

        self.event.clear()

    def run_speed_detection(self, event):

        detection_handler = DetectionHandler()

        while not event.is_set():
            result = detection_handler.run_detection()

            if result:
                self.set_current_limit(detection_handler.get_current_limit())

            Clock.schedule_once(partial(self.set_current_image, detection_handler.get_preview_image()))

    def set_current_speed(self, value):
        self.current_speed = value
        self.ids.current_speed_value.text = str(value)

    def set_current_limit(self, value):
        self.current_limit = value
        self.ids.current_limit_value.text = str(value)

    @mainthread
    def set_current_throttle(self, value):
        if value is None or value < 0:
            return

        self.current_throttle = value
        self.ids.throttle_slider.value_normalized = value * 0.01

    @mainthread
    def set_current_brake(self, value):
        self.current_brake = value
        self.ids.brake_slider.value_normalized = value * 0.01

    @mainthread
    def set_current_image(self, image, dt):
        helpers.PreviewImageHandler(image, self.ids.preview_image).resize_for_preview().update_texture()

    def update_current_throttle(self):
        throttle = LocomotiveController(None).calculate_throttle(int(self.current_limit), int(self.current_speed))
        if throttle < 0:
            throttle = 0
        self.set_current_throttle(throttle)

    def update_current_brake(self):
        value = self.ids.brake_slider.value_normalized * 100

        print(value)

        self.set_current_speed(int(value))
        self.update_current_throttle()


class SpeedControllerApp(MDApp):
    def build(self):
        Window.size = (1260, 720)

        Builder.load_file('gui/layouts/main_interface.kv')
        Builder.load_file('gui/layouts/settings_menu.kv')

        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
