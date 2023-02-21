from kivy.uix.popup import Popup

import utils.settings as s
import utils.utilities as utilities


class SettingsPopup(Popup):

    settings_manager = s.Settings()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for ident, element in self.ids.items():
            if utilities.is_text_input(element):
                element.text = self.settings_manager.get_setting_value(ident)

    def show_settings(self):
        self.open()

    def save_settings(self):
        for ident, element in self.ids.items():
            if utilities.is_text_input(element):
                self.settings_manager.set_setting_value(ident, element.text)

        self.settings_manager.write_to_file()
        self.dismiss()
