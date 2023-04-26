import time
from kivy.properties import partial
from kivy.clock import mainthread, Clock
from kivymd.app import MDApp
from kivy.base import Builder
from kivy.uix.widget import Widget
from interfaces import NotificationType, Subscriber
from application_core import SystemCore
from gui.settings_controller import SettingsMenuContent
from kivy.core.window import Window
import utils.helpers as helpers
from detection_system.detection_and_identification_system import DetectionHandler
from control_system.locomotive_controller import LocomotiveControlCore
from control_system.control_system import TrainSimClassicAdapter


class InterfaceController(Widget, Subscriber):
    application_core: SystemCore = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        sim_connector = TrainSimClassicAdapter()
        control_core = LocomotiveControlCore(sim_connector)
        control_core.register(self)

        detection_handler = DetectionHandler()
        detection_handler.register(self, control_core)

        self.application_core = SystemCore(control_core, detection_handler)

    def notify(self, event_type: NotificationType, value):
        if event_type == NotificationType.THROTTLE_POSITION:
            Clock.schedule_once(partial(self.set_current_throttle, value))
        elif event_type == NotificationType.BRAKE_POSITION:
            Clock.schedule_once(partial(self.set_current_brake, value))
        elif event_type == NotificationType.SPEED_LIMIT:
            Clock.schedule_once(partial(self.set_current_limit, value))
        elif event_type == NotificationType.SPEED_MPH:
            Clock.schedule_once(partial(self.set_current_speed, round(value, 1)))
        elif event_type == NotificationType.PREVIEW_IMAGE:
            Clock.schedule_once(partial(self.set_current_image, value))

    def open_settings(self):
        SettingsMenuContent().show_password_dialog()

    def begin_detection(self):
        self.set_stop_detection_button_enabled(True)
        self.set_start_detection_button_enabled(False)

        self.application_core.startup()

    def halt_detection(self):
        self.set_stop_detection_button_enabled(False)
        self.set_start_detection_button_enabled(True)

        self.application_core.shutdown()

    def emergency_stop(self):
        self.set_stop_detection_button_enabled(False)
        self.set_start_detection_button_enabled(True)

        self.application_core.shutdown()

    def set_start_detection_button_enabled(self, enabled_disabled: bool) -> None:
        self.ids.start_detection_button.disabled = not enabled_disabled

    def set_stop_detection_button_enabled(self, enabled_disabled: bool) -> None:
        self.ids.stop_detection_button.disabled = not enabled_disabled

    def set_current_speed(self, value, dt=None):
        self.ids.current_speed_value.text = str(value)

    def set_current_limit(self, value, t=None):
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


class SpeedControllerApp(MDApp):
    def build(self):
        Window.size = (1260, 720)

        Builder.load_file('gui/layouts/main_interface.kv')
        Builder.load_file('gui/layouts/settings_menu.kv')

        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
