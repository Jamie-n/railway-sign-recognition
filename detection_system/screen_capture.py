import mss
import numpy
import utils.settings as settings


class ScreenCapture:
    capture_height = int
    capture_width = int
    capture_offset = int

    def __init__(self, capture_height, capture_width):
        self.capture_height = capture_height
        self.capture_width = capture_width

    @staticmethod
    def load_from_settings():
        settings_helper = settings.Settings()
        return ScreenCapture(
            capture_height=settings_helper.get_setting_value('CAPTURE_HEIGHT'),
            capture_width=settings_helper.get_setting_value('CAPTURE_WIDTH')
        )

    def capture_frame(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": int(self.capture_width), "height": int(self.capture_height)}
            return numpy.array(sct.grab(monitor))
