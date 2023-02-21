from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from gui.settings_controller import SettingsPopup

class InterfaceController(Widget):

    def open_settings(self):
        SettingsPopup().show_settings()

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

        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
