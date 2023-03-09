import numpy
import pytesseract as pytesseract
from ultralytics import YOLO
import cv2
import utils.constants as constants
from detection_system.image_detection import ImageDetection


class FrameProcessor:
    def processFrame(self, frame):
        pass


class DetectionSystem(FrameProcessor):
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

        if len(detections.get_detections()) == 0:
            return

        first_detection = first_detection[0]
        frame = frame[first_detection.y1:first_detection.y2, first_detection.x1:first_detection.x2]

        detected_speed = pytesseract.image_to_string(ImageFilter(frame).filter_image(), config='--psm 9 -c tessedit_char_whitelist=0123456789')

        if detected_speed is None:
            return 00

        return detected_speed


class ImageFilter:
    image = []

    def __init__(self, image):
        self.image = image


    def filter_image(self):
        return cv2.resize(self.image, (300, 300), cv2.INTER_AREA)
