import cv2
from kivy.graphics.texture import Texture


class ImageHelpers:
    @staticmethod
    def image_to_texture(image):
        image_array = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_array = cv2.flip(image_array, 0)

        w, h, _ = image_array.shape
        texture = Texture.create(size=(h, w))

        texture.blit_buffer(image_array.flatten(), colorfmt='rgb', bufferfmt='ubyte')

        return texture

    @staticmethod
    def resize_image(image, width, height):
        return cv2.resize(image, dsize=(int(width), int(height)), interpolation=cv2.INTER_AREA)


class PreviewImageHandler:
    image_for_preview = []
    preview_image_window = None

    def __init__(self, image, preview_image_window):
        self.image_for_preview = image
        self.preview_image_window = preview_image_window

    def resize_for_preview(self):
        self.image_for_preview = ImageHelpers.resize_image(self.image_for_preview, self.preview_image_window.width, self.preview_image_window.height)
        return self

    def get_texture(self):
        return self.image_to_texture()

    def update_texture(self):
        self.preview_image_window.texture = self.image_to_texture()

    def image_to_texture(self):
        return ImageHelpers.image_to_texture(self.image_for_preview)


# Proportional, Integral, Derivative controller adapted from the formula listed on PID Explained, here:https://pidexplained.com/pid-controller-explained/
class PID:
    GAIN = 5.5
    CYCLE_TIME = 0.01
    previous_error = 0.0

    def __init__(self):
        pass

    def __call__(self, set_point: int, process_value: int) -> float:
        error = set_point - process_value

        p = self.GAIN * error
        i = self.GAIN * error * self.CYCLE_TIME
        d = self.GAIN * 0 / self.CYCLE_TIME

        self.previous_error = error

        val = p + i + d

        return val
