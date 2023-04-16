import mss
import numpy
import cv2
import utils.settings_helper as settings
import utils.constants as constants
from pygrabber.dshow_graph import FilterGraph


class ScreenCapture:
    capture_height = int
    capture_width = int

    cv2_video_capture = None

    def __init__(self, capture_height, capture_width, capture_device_name=None):
        self.capture_height = capture_height
        self.capture_width = capture_width
        self.cv2_video_capture = cv2.VideoCapture(ScreenCapture.capture_device_name_to_index(capture_device_name), cv2.CAP_DSHOW)

        self.cv2_video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cv2_video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    @staticmethod
    def load_from_settings():
        settings_helper = settings.Settings()
        return ScreenCapture(
            capture_height=settings_helper.get_setting_value('CAPTURE_HEIGHT'),
            capture_width=settings_helper.get_setting_value('CAPTURE_WIDTH'),
            capture_device_name=settings.Settings().get_setting_value('CAPTURE_DEVICE')
        )

    def capture_preview_frame(self):
        cv2.imwrite(constants.CAPTURE_PREVIEW_PATH, self.capture_frame())

    def capture_frame(self):
        if self.cv2_video_capture.isOpened():
            ret, frame = self.cv2_video_capture.read()
            cropped = frame[0:int(self.capture_width), 0:int(self.capture_height)]
            return cropped

        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": int(self.capture_width), "height": int(self.capture_height)}
            return numpy.array(sct.grab(monitor))

    @staticmethod
    def get_capture_devices():
        graph = FilterGraph()
        return graph.get_input_devices()

    @staticmethod
    def capture_device_name_to_index(device_name):
        devices = ScreenCapture.get_capture_devices()

        try:
            return devices.index(device_name)
        except ValueError:
            return None
