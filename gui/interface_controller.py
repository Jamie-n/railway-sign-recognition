from datetime import datetime

import cv2
import threading
import time
from threading import Event

from kivy.properties import partial

import detection_system.screen_capture as screen_capture
from detection_system.screen_capture import ScreenCapture
from kivy.clock import mainthread, Clock
from kivymd.app import MDApp
from kivy.base import Builder
from kivy.uix.widget import Widget
from gui.settings_controller import SettingsMenuContent
from kivy.core.window import Window
import utils.helpers as helpers
from detection_system.detection_and_identification_system import DetectionSystem, IdentificationSystem

class InterfaceController(Widget):
    event = Event()
    thread = None

    current_speed = 00
    current_limit = 00
    current_throttle = 00
    current_brake = 00

    frames_since_detection = 0

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
        self.ids.current_limit_value.text = "00"

        self.event.set()

        self.thread.join()

        self.event.clear()

    def run_speed_detection(self, event):

        detector = DetectionSystem()

        while not event.is_set():
            start_time = time.time()

            image = ScreenCapture.load_from_settings().capture_frame()

            detection = detector.process_frame(image)

            image = detection.get_image()

            speed = IdentificationSystem().process_frame(detection)

            preview_image = self.ids.preview_image
            resized_image = cv2.resize(image, dsize=(int(preview_image.width), int(preview_image.height)), interpolation=cv2.INTER_AREA)

            Clock.schedule_once(partial(self.set_current_image, resized_image))
            self.set_current_speed(speed)

            print("FPS: ", 1.0 / (time.time() - start_time))


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
    def set_current_image(self, value, dt):
        texture = screen_capture.convert_to_texture(value)
        self.ids.preview_image.texture = texture


class SpeedControllerApp(MDApp):
    def build(self):
        Window.size = (1260, 720)

        Builder.load_file('gui/layouts/main_interface.kv')
        Builder.load_file('gui/layouts/settings_menu.kv')

        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
