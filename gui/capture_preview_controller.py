import numpy
from kivy.uix.popup import Popup
import detection_system.screen_capture as capture
import utils.constants as constants


class CapturePreviewPopup(Popup):

    def show_preview(self, capture_width, capture_height):
        screen_capture = capture.ScreenCapture(capture_width=capture_width, capture_height=capture_height)
        screen_capture.capture_preview_frame()

        self.ids.preview_image.source = constants.CAPTURE_PREVIEW_PATH
        self.open()
