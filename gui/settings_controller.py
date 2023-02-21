import json
from utils import constants
from kivy.uix.popup import Popup


def get_settings_from_file():
    with open(constants.SETTINGS_PATH) as json_file:
        return json.load(json_file)


class SettingsPopup(Popup):
    settings_dict = dict
    capture_height_input = ''
    capture_width_input = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture_height_input = self.ids.capture_height_input
        self.capture_width_input = self.ids.capture_width_input

    def show_settings(self):
        self.open()
        self.settings_dict = get_settings_from_file()

        self.capture_height_input.text = self.get_setting(constants.CAPTURE_HEIGHT)
        self.capture_width_input.text = self.get_setting(constants.CAPTURE_WIDTH)


    def save_settings(self):

        self.set_setting(constants.CAPTURE_HEIGHT, self.ids.capture_height_input.text)
        print(self.settings_dict)
        self.dismiss()

    def get_setting(self, value: str):
        return str(self.settings_dict[value])

    def set_setting(self, key: str, value: str):
        self.settings_dict[key] = value

