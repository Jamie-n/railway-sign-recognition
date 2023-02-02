import mss
import numpy
from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

img = cv2.imread('test.jpg')


def detect(image):
    return model(image)


with mss.mss() as sct:
    while True:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))
        image_without_alpha = img[:, :, :3]

        results = detect(image_without_alpha)

        result = results[0]

        boxes = result.boxes
        test = boxes.xyxy.numpy()

        if len(test) > 0:
            x1, y1, x2, y2 = test[0]
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        cv2.imshow("Output Window", img)
        cv2.waitKey(250)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
