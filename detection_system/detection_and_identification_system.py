import time

import pytesseract as pytesseract
from ultralytics import YOLO
import cv2
import utils.constants as constants
from detection_system.image_detection import ImageDetection
from detection_system.screen_capture import ScreenCapture
from interfaces import Publisher, NotificationType
from utils.settings_helper import Settings


class DetectionHandler(Publisher):
    current_frame = []
    current_limit = 0

    detector = None
    screen_capture = None
    digit_ident = None
    is_debug = False

    def __init__(self):
        self.detector = DetectionSystem()
        self.is_debug = Settings().is_debug()
        self.digit_ident = IdentificationSystem()

    def run(self, event):
        self.screen_capture = ScreenCapture.load_from_settings()

        while not event.isSet():
            start_time = time.time()
            detection = self.detector.process_frame(self.screen_capture.capture_frame())
            self.current_frame = detection.get_image()

            self.emit(NotificationType.PREVIEW_IMAGE, self.current_frame)

            # If the detection subnet has detected a speed sign, calculate the speed stated, if a speed was detected within the expected values inform the interface to update
            if detection.has_detections():
                speed = self.digit_ident.process_frame(detection)

                if speed is not None:
                    self.set_current_limit(speed)

            if self.is_debug:
                print("Time of Last Detection Cycle: ", round((time.time() - start_time) * 1000, 3), "ms")


        self.set_current_limit(0.0)

    def get_preview_image(self):
        return self.current_frame

    def get_current_limit(self):
        return self.current_limit

    def set_current_limit(self, speed):
        self.current_limit = speed
        self.emit(NotificationType.SPEED_LIMIT, speed)


class FrameProcessor:
    def processFrame(self, frame):
        pass


class DetectionSystem(FrameProcessor, Publisher):
    model = YOLO

    def __init__(self):
        self.model = YOLO(constants.PRETRAINED_MODEL_PATH)

    def process_frame(self, captured_frame):
        # Take the alpha layer out of the captured frame (Not used)
        image_without_alpha_channel = captured_frame[:, :, :3]

        results = self.model(image_without_alpha_channel)

        # Generate a container object storing the image & the bounding boxes of all the results
        image_detection = ImageDetection().generate_from_results(captured_frame, results)

        for box in image_detection.get_detections():
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(captured_frame, str(box.certainty), box.top_left(), font, 1, (0, 255, 0), 4, cv2.LINE_AA)
            cv2.rectangle(captured_frame, box.top_left(), box.bottom_right(), (0, 255, 0), 2)

        return image_detection


class IdentificationSystem(FrameProcessor):

    def process_frame(self, detections):
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        frame = detections.get_image()

        first_detection = detections.get_detections()

        first_detection = first_detection[0]
        frame = frame[first_detection.y1:first_detection.y2, first_detection.x1:first_detection.x2]

        detected_speed = pytesseract.image_to_string(ImageFilter(frame).filter_image(), config='--psm 9 -c tessedit_char_whitelist=0123456789')

        return self.filter_detected_speed(detected_speed)

    @staticmethod
    def filter_detected_speed(detected_speed):
        try:
            if int(detected_speed) in constants.ACCEPTED_SPEED_VALUES:
                return detected_speed
        except:
            return None


class ImageFilter:
    image = []

    def __init__(self, image):
        self.image = image

    def filter_image(self):
        return cv2.resize(self.image, (300, 300), cv2.INTER_AREA)
