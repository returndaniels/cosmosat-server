import os
import cv2
from datetime import datetime
from multiprocessing import Process
from api import crud
from app.ws import ConnectionManager
from core.detection import LightningDetect

ws = ConnectionManager.instance()


async def save_data_func(detection_id, centroid_x, centroid_y, size, timestamp):
    crud.create_lightning(timestamp, size, centroid_x, centroid_y, detection_id)
    await ws.broadcast(
        {
            "timestamp": timestamp,
            "centroid_x": centroid_x,
            "centroid_y": centroid_y,
            "size": size,
        }
    )


def save_frame_func(detection_id, frame, timestamp):
    dir_name = f"detection_{detection_id}"

    home_dir = os.path.expanduser("~")
    dir_path = os.path.join(home_dir, dir_name)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    filename = f"frame_{timestamp}.jpg"
    cv2.imwrite(os.path.join(dir_path, filename), frame)


async def listen_pipe(process: Process, pipe):
    while process.is_alive():
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        detection_id, cx, cy, size, frame = pipe.recv()
        await save_data_func(detection_id, cx, cy, size, timestamp)
        save_frame_func(detection_id, frame, timestamp)
    pipe.close()


def start_detection(pipe):
    now = datetime.now()
    start_time = datetime.timestamp(now)
    detection_id = crud.create_detection_record(start_time)
    detect = LightningDetect(detection_id, pipe)
    detect.detecting_process()
