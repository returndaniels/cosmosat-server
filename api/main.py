import os
import cv2
from datetime import datetime
from multiprocessing import Process
from api import crud
from app.ws import ConnectionManager
from core.detection import LightningDetect

ws = ConnectionManager.instance()


async def save_data_func(detection_id, centroid_x, centroid_y, size, timestamp):
    """Salva dados de detecção de relâmpago no banco de dados e transmite via WebSocket.

    Args:
        detection_id (str): Identificador único da detecção.
        centroid_x (int): Coordenada x do centroide do relâmpago.
        centroid_y (int): Coordenada y do centroide do relâmpago.
        size (int): Tamanho do relâmpago.
        timestamp (float): Timestamp da detecção.
    """

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
    """Salva um frame de vídeo em disco com a detecção de relâmpago.

    Args:
      detection_id (str): Identificador único da detecção.
      frame (numpy.ndarray): Frame de vídeo a ser salvo.
      timestamp (float): Timestamp da detecção.
    """

    base_dir = os.path.join(os.path.expanduser("~"), "imagens_deteccao")
    dir_path = os.path.join(base_dir, f"deteccao_{detection_id}")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    filename = f"frame_{timestamp}.jpg"
    cv2.imwrite(os.path.join(dir_path, filename), frame)


async def listen_pipe(process: Process, pipe):
    """Escuta um pipe para receber dados de detecção de relâmpago.

    Args:
        process (Process): Processo de detecção de relâmpago.
        pipe: Pipe de comunicação com o processo de detecção.
    """

    while process.is_alive():
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        detection_id, cx, cy, size, frame = pipe.recv()
        await save_data_func(detection_id, cx, cy, size, timestamp)
        save_frame_func(detection_id, frame, timestamp)
    pipe.close()


def start_detection(pipe):
    """Inicia um processo de detecção de relâmpago.

    Args:
        pipe: Pipe de comunicação com o processo de detecção.
    """

    now = datetime.now()
    start_time = datetime.timestamp(now)
    detection_id = crud.create_detection_record(start_time)
    detect = LightningDetect(detection_id, pipe)
    detect.detecting_process()
