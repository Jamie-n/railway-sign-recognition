import utils.constants as constants
import json


class Settings:
    settings_dictionary = dict

    def __init__(self):
        try:
            with open(constants.SETTINGS_PATH) as settings_file:
                self.settings_dictionary = json.load(settings_file)
        except ValueError:
            self.settings_dictionary = {}

    def get_setting_value(self, key: str):
        if key not in self.settings_dictionary.keys():
            return ''

        return self.settings_dictionary[key]

    def set_setting_value(self, key: str, value: str) -> None:
        self.settings_dictionary[key] = value

    def write_to_file(self) -> None:
        with open(constants.SETTINGS_PATH, "w") as settings_file:
            json.dump(self.settings_dictionary, settings_file)

    def get_password(self) -> str:
        return self.get_setting_value('PASSCODE')

    def is_debug(self) -> bool:
        return self.get_setting_value('IS_DEBUG')
