from typing import List

from numpy import array


class DetectionBox:
    x1 = int
    x2 = int
    y1 = int
    y2 = int
    certainty = int

    def __init__(self, x1, y1, x2, y2, certainty):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.certainty = certainty

    @staticmethod
    def from_box(box):
        x1, y1, x2, y2 = box.xyxy.numpy()[0]
        return DetectionBox(x1, y1, x2, y2, box.conf.numpy()[0])

    def top_left(self):
        return (self.x1, self.y1)

    def bottom_right(self):
        return (self.x2, self.y2)


class ImageDetection:
    image = array
    detections = [DetectionBox]

    def __init__(self, image=array, detections=List):
        self.image = image
        self.detections = detections

    def get_image(self):
        return self.image

    def get_detections(self):
        return self.detections

    def has_detections(self):
        return len(self.detections) > 0

    @staticmethod
    def generate_from_results(image, results):
        results_list = []
        for result in results:
            for box in result.boxes:
                results_list.append(DetectionBox.from_box(box))

        return ImageDetection(image, results_list)
