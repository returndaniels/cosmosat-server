from pydantic import BaseModel


class Lightning(BaseModel):
    def __init__(self, id, detection_id, timestamp, size, centroid_x, centroid_y):
        self.id = id
        self.detection_id = detection_id
        self.timestamp = timestamp
        self.size = size
        self.centroid_x = centroid_x
        self.centroid_y = centroid_y


class DetectionRecord(BaseModel):
    def __init__(self, id, start_time):
        self.id = id
        self.start_time = start_time
