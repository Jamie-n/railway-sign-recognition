from ultralytics import YOLO
import cv2
import utils.constants as constants


class DetectionSystem:
    model = YOLO

    def __init__(self):
        self.model = YOLO(constants.PRETRAINED_MODEL_PATH)

    def process_frame(self, captured_frame):
        # Take the alpha layer out of the captured frame (Not used)
        image_without_alpha_channel = captured_frame[:, :, :3]

        results = self.model(image_without_alpha_channel)

        for result in results:

            boxes = result.boxes
            test = boxes.xyxy.numpy()

            if len(test) > 0:
                x1, y1, x2, y2 = test[0]
                cv2.rectangle(captured_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        cv2.imwrite(constants.CAPTURE_PREVIEW_PATH, captured_frame)

        return captured_frame
