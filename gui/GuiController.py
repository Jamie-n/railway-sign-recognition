from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup


class SettingsPopup(Popup):
    def save_settings(self):
        self.dismiss()


class MyGridLayout(Widget):

    def open_settings(self):
        SettingsPopup().open()

    def begin_detection(self):
        self.ids.stop_detection_button.disabled = False
        self.ids.start_detection_button.disabled = True

    def halt_detection(self):
        self.ids.start_detection_button.disabled = False
        self.ids.stop_detection_button.disabled = True
        self.ids.current_limit_value.text = "00"


class SpeedControllerApp(App):
    def build(self):
        Window.size = (1260, 720)

        return MyGridLayout()


def initialize():
    SpeedControllerApp().run()
