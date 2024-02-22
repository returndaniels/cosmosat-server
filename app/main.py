from fastapi import Request, HTTPException, WebSocket, WebSocketDisconnect

from datetime import datetime
from multiprocessing import Process

from api import crud
from api.main import save_data_func, save_frame_func, stop_detection
from app import app, templates
from app.ws import ConnectionManager
from core.detection import LightningDetect

ws = ConnectionManager()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/camera-status")
def get_cam_status():
    return {"status": "enabled"}


@app.get("/start-detection")
async def get_start_detection():
    try:
        now = datetime.now()
        start_time = datetime.timestamp(now)
        detection_id = crud.create_detection_record(start_time)

        def detection_process():
            detect = LightningDetect(detection_id, save_data_func, save_frame_func)
            detect.detecting_process()

        process = Process(target=detection_process)
        process.start()
        return {"status": "ok", "code": 200, "detail": "Detecção iniciada"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str("Iniciar a adetecção falhou."))


@app.get("/stop-detection")
def get_stop_detection():
    if stop_detection() == 200:
        return {"status": "ok", "code": 200, "detail": "Detecção encerrada"}
    else:
        raise HTTPException(status_code=500, detail=str("Falha na requisição"))


@app.get("/detections")
def get_all_detections():
    try:
        return crud.get_all_detection_records()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/detections/{id}")
def get_detection(id: int):
    try:
        return crud.get_detection_record(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/detections/{id}")
def delete_detection(id: int):
    try:
        crud.delete_detection_record(id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws-connect/")
async def ws_connect(websocket: WebSocket):
    await ws.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("ws message:", data)
    except WebSocketDisconnect:
        ws.disconnect(websocket)
