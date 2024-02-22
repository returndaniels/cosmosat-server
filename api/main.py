import os
import signal
from api import crud
from datetime import datetime

from core.detection import LightningDetect

pid = None


def save_data_func(detection_id, centroid_x, centroid_y, size):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    crud.create_lightning(timestamp, size, centroid_x, centroid_y, detection_id)


def save_frame_func(frame):
    pass


def start_detection():
    now = datetime.now()
    start_time = datetime.timestamp(now)
    detection_id = crud.create_detection_record(start_time)
    detect = LightningDetect(detection_id, save_data_func, save_frame_func)

    if not detect.pid:
        detect.detecting_process()

    # Iniciar streamer de dados
    # ...


def stop_detection():
    try:
        detect = LightningDetect()
        os.kill(detect.pid, signal.SIGTERM)
        detect.pid = None
        print(f"Sent SIGTERM signal to process {pid}")
    except OSError:
        print(f"Failed to send SIGTERM signal to process {pid}")
    # Parar streamer de dados
    # ...
