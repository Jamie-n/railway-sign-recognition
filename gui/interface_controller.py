import threading
import time
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
from control_system.locomotive_controller import LocomotiveControlCore
from control_system.control_system import TrainSimClassicAdapter


class InterfaceController(Widget):
    event = Event()
    detection_thread = None
    control_thread = None

    current_speed = 00
    current_limit = 00

    locomotive_controller = None
    detection_handler = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sim_connector = TrainSimClassicAdapter()
        self.locomotive_controller = LocomotiveControlCore(sim_connector, self)
        self.detection_handler = DetectionHandler()

    def open_settings(self):
        SettingsMenuContent().show_settings()

    def begin_detection(self):
        self.set_stop_detection_button_enabled(True)
        self.set_start_detection_button_enabled(False)

        self.locomotive_controller.connect()

        self.detection_thread = threading.Thread(target=self.run_speed_detection, args=(self.event,), daemon=True)
        self.control_thread = threading.Thread(target=self.run_locomotive_control, args=(self.event,), daemon=True)

        self.detection_thread.start()
        self.control_thread.start()

    def halt_detection(self):
        self.set_stop_detection_button_enabled(False)
        self.set_start_detection_button_enabled(True)

        self.locomotive_controller.disconnect()

        self.event.set()

        self.detection_thread.join()
        self.control_thread.join()

        self.event.clear()

    def set_start_detection_button_enabled(self, enabled_disabled: bool) -> None:
        self.ids.start_detection_button.disabled = not enabled_disabled

    def set_stop_detection_button_enabled(self, enabled_disabled: bool) -> None:
        self.ids.stop_detection_button.disabled = not enabled_disabled

    def run_speed_detection(self, event):
        while not event.is_set():
            result = self.detection_handler.run()

            if result:
                self.set_current_limit(self.detection_handler.get_current_limit())

            Clock.schedule_once(partial(self.set_current_image, self.detection_handler.get_preview_image()))

    def run_locomotive_control(self, event):
        while not event.isSet():
            self.locomotive_controller.control_speed(self.current_limit)

            Clock.schedule_once(partial(self.set_current_speed, round(self.locomotive_controller.get_speed())), 1)
            Clock.schedule_once(partial(self.set_current_throttle, self.locomotive_controller.get_throttle()))
            Clock.schedule_once(partial(self.set_current_brake,self.locomotive_controller.get_brake()))

            time.sleep(0.1)

    def set_current_speed(self, value, dt):
        self.current_speed = value
        self.ids.current_speed_value.text = str(value)

    def set_current_limit(self, value, t=None):
        self.current_limit = value
        self.ids.current_limit_value.text = str(value)

    @mainthread
    def set_current_throttle(self, value: float, t):
        self.ids.throttle_slider.value_normalized = value

    @mainthread
    def set_current_brake(self, value, t):
        self.ids.brake_slider.value_normalized = value

    @mainthread
    def set_current_image(self, image, t):
        helpers.PreviewImageHandler(image, self.ids.preview_image).resize_for_preview().update_texture()

    def update_current_throttle(self):
        pass

    def update_current_brake(self):
        pass


class SpeedControllerApp(MDApp):
    def build(self):
        Window.size = (1260, 720)

        Builder.load_file('gui/layouts/main_interface.kv')
        Builder.load_file('gui/layouts/settings_menu.kv')

        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
