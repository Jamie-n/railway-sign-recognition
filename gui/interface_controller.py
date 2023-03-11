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

        detection_handler = DetectionHandler()
        self.thread = threading.Thread(target=self.run_speed_detection, args=(self.event, detection_handler,), daemon=True)

        self.thread.start()

    def halt_detection(self):
        self.ids.start_detection_button.disabled = False
        self.ids.stop_detection_button.disabled = True

        self.event.set()

        self.thread.join()

        self.event.clear()

    def run_speed_detection(self, event, detection_handler):

        while not event.is_set():
            result = detection_handler.run_detection()

            if result:
                self.set_current_limit(detection_handler.get_current_limit())

            Clock.schedule_once(partial(self.set_current_image, detection_handler.get_preview_image()))

    def set_current_speed(self, value):
        self.current_speed = value
        self.ids.current_speed_value.text = helpers.pad_digits(str(value))

    def set_current_limit(self, value):
        self.current_limit = value
        self.ids.current_limit_value.text = str(helpers.pad_digits(str(value)))

    @mainthread
    def set_current_throttle(self, value):
        self.current_throttle = value
        self.ids.throttle_slider.value_normalized = value * 0.01

    @mainthread
    def set_current_brake(self, value):
        self.current_brake = value
        self.ids.brake_slider.value_normalized = value * 0.01

    @mainthread
    def set_current_image(self, image, dt):
        helpers.PreviewImageHandler(image, self.ids.preview_image).resize_for_preview().update_texture()


class SpeedControllerApp(MDApp):
    def build(self):
        Window.size = (1260, 720)

        Builder.load_file('gui/layouts/main_interface.kv')
        Builder.load_file('gui/layouts/settings_menu.kv')

        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
