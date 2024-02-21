from datetime import datetime

class Lightning:
  def __init__(self, id, momment, size, centroid_x, centroid_y):
    self.id = id
    self.momment = momment
    self.size = size
    self.centroid_x = centroid_x
    self.centroid_y = centroid_y
  
  @property
  def momment_str(self):
    return datetime.fromtimestamp(self.momment).strftime("%Y-%m-%d %H:%M:%S")

class DetectionRecord:
  def __init__(self, id, start_time):
    self.id = id
    self.start_time = start_time

  @property
  def start_time_str(self):
    return datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S")
