import asyncio
from fastapi import Request, HTTPException, WebSocket, WebSocketDisconnect

from multiprocessing import Pipe, Process

from api import crud
from api.main import listen_pipe, start_detection, stop_detection
from app import app, templates
from app.ws import ConnectionManager

ws = ConnectionManager()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/camera-status")
def get_cam_status():
    return {"status": "enabled"}


@app.get("/start-detection")
def get_start_detection():
    try:
        parent_pipe, child_pipe = Pipe()
        process = Process(target=start_detection, args=(child_pipe,))
        process.start()

        asyncio.run(listen_pipe(process, parent_pipe))

        return {"status": "ok", "code": 200, "detail": "Detecção iniciada"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Iniciar a adetecção falhou.")


@app.get("/stop-detection")
def get_stop_detection():
    try:
        stop_detection()
        return {"status": "ok", "code": 200, "detail": "Detecção encerrada"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha na requisição")


@app.get("/detections")
def get_all_detections():
    try:
        return crud.get_all_detection_records()
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha ao bsucar detecções.")


@app.get("/detections/{id}")
def get_detection(id: int):
    try:
        return crud.get_detection_record(id)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha ao bsucar detecção.")


@app.delete("/detections/{id}")
def delete_detection(id: int):
    try:
        crud.delete_detection_record(id)
        return {"success": True}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha ao apagar detecção.")


@app.websocket("/ws-connect/")
async def ws_connect(websocket: WebSocket):
    await ws.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("ws message:", data)
    except WebSocketDisconnect:
        ws.disconnect(websocket)
