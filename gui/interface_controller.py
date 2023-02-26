from kivymd.app import MDApp
from kivy.base import Builder
from kivy.uix.widget import Widget
from gui.settings_controller import SettingsMenuContent
from kivy.core.window import Window

class InterfaceController(Widget):

    def open_settings(self):
        SettingsMenuContent().show_settings()

    def begin_detection(self):
        self.ids.stop_detection_button.disabled = False
        self.ids.start_detection_button.disabled = True

    def halt_detection(self):
        self.ids.start_detection_button.disabled = False
        self.ids.stop_detection_button.disabled = True
        self.ids.current_limit_value.text = "00"


class SpeedControllerApp(MDApp):
    def build(self):
        Window.size = (1260, 720)

        Builder.load_file('gui/layouts/main_interface.kv')
        Builder.load_file('gui/layouts/settings_menu.kv')
        Builder.load_file('gui/layouts/capture_preview.kv')


        return InterfaceController()


def initialize():
    SpeedControllerApp().run()
