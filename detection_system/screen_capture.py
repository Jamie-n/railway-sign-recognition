import mss
import numpy
import cv2
from kivy.clock import mainthread
from numpy import array
import utils.settings as settings
import utils.constants as constants
from kivy.graphics.texture import Texture


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

    def capture_preview_frame(self):
        cv2.imwrite(constants.CAPTURE_PREVIEW_PATH, self.capture_frame())

    def capture_frame(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": int(self.capture_width), "height": int(self.capture_height)}
            return numpy.array(sct.grab(monitor))



def convert_to_texture(image_array):
    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    image_array = cv2.flip(image_array, 0)

    w, h, _ = image_array.shape
    texture = Texture.create(size=(h, w))
    texture.blit_buffer(image_array.flatten(), colorfmt='rgb', bufferfmt='ubyte')

    return texture
