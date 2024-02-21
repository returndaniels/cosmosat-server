from api import crud
from api.models import DetectionRecord
from time import time


def start_detection():
    # Iniciar script de detecção de raios
    # ...

    start_time = time()
    crud.create_detection_record(start_time)

    # Iniciar streamer de dados
    # ...


def stop_detection():
    # Parar script de detecção de raios
    # ...

    # Parar streamer de dados
    # ...
    pass


if __name__ == "__main__":
    # Iniciar API FastAPI

    # Rotas para API RESTful
    # ...

    # Rotas para streamer de dados
    # ...

    # Iniciar detecção de raios
    start_detection()

    # Manter servidor em execução
    # ...
