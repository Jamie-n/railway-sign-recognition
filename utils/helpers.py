import cv2
from kivy.graphics.texture import Texture

def pad_digits(value=str):
    return value.zfill(2)

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
