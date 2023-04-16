from typing import Union

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
import detection_system.screen_capture as capture
import utils.helpers as helpers
from utils.settings_helper import Settings
from argon2 import PasswordHasher


class CapturePreview(BoxLayout):
    pass


class PasswordDialog(BoxLayout):
    pass


class SettingsMenuContent(BoxLayout):
    settings_manager = Settings()
    dialog = None
    preview_dialog = None
    password_dialog = None
    capture_device_menu = None

    def show_settings(self):
        self.dialog = MDDialog(
            title="System Settings:",
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_release=self.hide_settings
                ),
                MDFlatButton(
                    text="SAVE SETTINGS",
                    theme_text_color="Custom",
                    on_release=self.save_settings
                ),
            ],
        )

        for ident in self.dialog.content_cls.ids:
            element = self.dialog.content_cls.ids[ident]
            element.text = self.settings_manager.get_setting_value(ident)

        self.dialog.content_cls.ids.IS_DEBUG.active = self.settings_manager.is_debug()

        self.capture_device_menu = MDDropdownMenu(
            caller=self.dialog.content_cls.ids.CAPTURE_DEVICE,
            items=self.build_capture_device_list(),
            position="center",
            width_mult=4,
        )

        self.dialog.open()

    def hide_settings(self, *args):
        self.dialog.dismiss(force=True)

    def hide_preview(self, *args):
        self.preview_dialog.dismiss(force=True)

    def build_capture_device_list(self):
        menu_items = []
        devices = capture.ScreenCapture.get_capture_devices()+ ['Screen Capture']

        for device in devices:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": f"{device}",
                "on_release": lambda x=f"{device}": self.set_capture_device(x),
            })

        return menu_items

    def hide_password_dialog(self, *args):
        self.password_dialog.dismiss(force=True)

    def set_capture_device(self, capture_device_name):
        self.dialog.content_cls.ids.CAPTURE_DEVICE.text = capture_device_name
        self.capture_device_menu.dismiss()

    def is_password_valid(self, *args):
        self.password_dialog.content_cls.ids.PASSWORD.error = True
        passcode = self.password_dialog.content_cls.ids.PASSWORD.text

        try:
            if PasswordHasher().verify(self.settings_manager.get_password(), passcode):
                return True
        except VerifyMismatchError:
            return False

    def validate_password(self, *args):
        if self.is_password_valid() or self.settings_manager.is_debug():
            self.hide_password_dialog()
            self.show_settings()

        self.password_dialog.content_cls.ids.PASSWORD.error = True

    def show_password_dialog(self):
        self.password_dialog = MDDialog(
            title="Enter Passcode:",
            type="custom",
            content_cls=PasswordDialog(),
            buttons=[
                MDFlatButton(
                    text="Submit",
                    theme_text_color="Custom",
                    on_release=self.validate_password
                ),
                MDFlatButton(
                    text="Close",
                    theme_text_color="Custom",
                    on_release=self.hide_password_dialog
                ),
            ],
        )

        self.password_dialog.open()

    def save_settings(self, *args):
        for ident in self.dialog.content_cls.ids:
            element = self.dialog.content_cls.ids[ident]
            self.settings_manager.set_setting_value(ident, element.text)

        self.settings_manager.set_setting_value('IS_DEBUG', self.dialog.content_cls.ids.IS_DEBUG.active)

        self.settings_manager.write_to_file()
        self.hide_settings()

    def preview_capture(self):
        self.preview_dialog = MDDialog(
            title="Capture Preview:",
            type="custom",
            content_cls=CapturePreview(),
            buttons=[
                MDFlatButton(
                    text="Close",
                    theme_text_color="Custom",
                    on_release=self.hide_preview
                ),
            ],
        )

        self.preview_dialog.open()

        screen_capture = capture.ScreenCapture(capture_width=int(self.ids.CAPTURE_WIDTH.text), capture_height=int(self.ids.CAPTURE_HEIGHT.text), capture_device_name=self.ids.CAPTURE_DEVICE.text)
        preview_window = self.preview_dialog.content_cls.ids.preview_image

        helpers.PreviewImageHandler(screen_capture.capture_frame(), preview_window).resize_for_preview().update_texture()
