import asyncio
from datetime import datetime
from api import crud
from core.detection import LightningDetect


async def save_data_func(detection_id, centroid_x, centroid_y, size, ws):
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


def start_detection(ws):
    now = datetime.now()
    start_time = datetime.timestamp(now)
    detection_id = crud.create_detection_record(start_time)
    detect = LightningDetect(detection_id, save_data_func, save_frame_func, ws)
    asyncio.run(detect.detecting_process())

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
