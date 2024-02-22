import cv2
import numpy as np

from singleton import Singleton


class LightningDetect(Singleton):
    def __init__(self, detection_id=None, save_data_func=None, save_frame_func=None):
        """
        Creates a LightningDetect instance with optional configuration.

        Args:
            detection_id (str, optional): Unique identifier for the detection.
            save_data_func (callable, optional): Function to save detection data.
            save_frame_func (callable, optional): Function to save the video frame.

        If called without arguments, it accesses attributes from the existing instance.
        """

        # Allow accessing attributes on subsequent calls without arguments
        if not (detection_id or save_data_func or save_frame_func):
            return

        # Initialize attributes only on the first call with arguments
        self.pid = None
        self.detection_id = detection_id
        self.save_data_func = save_data_func
        self.save_frame_func = save_frame_func

        # Initialize resources in a protected method to avoid duplication
        self._initialize_resources()

    def _initialize_resources(self):
        """Initializes capture device and thresholds with proper error handling."""
        try:
            self.cap = cv2.VideoCapture(0)
            self.lower = np.array([80, 50, 50])
            self.upper = np.array([90, 255, 255])
        except (cv2.error, Exception) as e:
            print("Error initializing resources:", e)

    @classmethod
    def instance(cls):
        return cls()

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

                    # await self.save_data_func(self.detection_id, cx, cy, area)
                    self.save_frame_func(frame)

                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            cv2.imshow("Object Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
