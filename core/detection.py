import cv2
import numpy as np


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            instance = super(Singleton, class_).__new__(class_)
            class_._instances[class_] = instance
        return class_._instances[class_]


class LightningDetect(Singleton):
    def __init__(self, detection_id, save_data_func, save_frame_func):
        self.detection_id = detection_id
        self.save_data_func = save_data_func
        self.save_frame_func = save_frame_func

        self.cap = cv2.VideoCapture(0)
        self.lower = np.array([80, 50, 50])
        self.upper = np.array([90, 255, 255])

    def find_centroid(self, contour):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY
        else:
            return 0, 0

    def detecting_process(self):
        while True:
            ret, frame = self.cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            part_mask = cv2.inRange(hsv, self.lower, self.upper)
            mask = cv2.bitwise_or(part_mask, part_mask)
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)

                if area > 500:
                    cx, cy = self.find_centroid(contour)

                    self.save_data_func(self.detection_id, cx, cy, area)
                    self.save_frame_func(frame)

                    # cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                    # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            cv2.imshow("Object Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
