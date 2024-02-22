from datetime import datetime
from multiprocessing import Process
from api import crud
from app.ws import ConnectionManager
from core.detection import LightningDetect

ws = ConnectionManager.instance()


async def save_data_func(detection_id, centroid_x, centroid_y, size):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    crud.create_lightning(timestamp, size, centroid_x, centroid_y, detection_id)
    await ws.broadcast(
        {
            "timestamp": timestamp,
            "centroid_x": centroid_x,
            "centroid_y": centroid_y,
            "size": size,
        }
    )


def save_frame_func(frame):
    pass


async def listen_pipe(process: Process, pipe):
    while process.is_alive():
        detection_id, cx, cy, size, frame = pipe.recv()
        await save_data_func(detection_id, cx, cy, size)
        await save_frame_func(frame)
    pipe.close()


def start_detection(pipe):
    now = datetime.now()
    start_time = datetime.timestamp(now)
    detection_id = crud.create_detection_record(start_time)
    detect = LightningDetect(detection_id, pipe)
    detect.detecting_process()

    # Optionally wait for process to finish before returning
    # process.join()


def stop_detection():
    try:
        detector = LightningDetect.instance()
        detector.kill_process()
        return 200
    except:
        return 500

    # Parar streamer de dados
    # ...
