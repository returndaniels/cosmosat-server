import asyncio
import picamera
from fastapi import Request, HTTPException, WebSocket, WebSocketDisconnect

from multiprocessing import Pipe, Process

from api import crud
from api.main import listen_pipe, start_detection
from app import app, templates
from app.ws import ConnectionManager

ws = ConnectionManager()
camera = picamera.PiCamera()
detection_process = None


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/camera-status")
def get_cam_status():
    """Retorna o status atual da câmera."""
    return {"status": "enabled" if camera.closed is False else "disabled"}


@app.post("/camera-status")
def toggle_cam_status():
    """Inverte o status da câmera (liga ou desliga)."""
    if camera.closed:
        camera.start_preview()
    else:
        camera.stop_preview()
        camera.close()

    return {"status": "enabled" if camera.closed is False else "disabled"}


@app.get("/start-detection")
def get_start_detection():
    try:
        global detection_process
        if detection_process is not None:
            raise HTTPException(status_code=400, detail="Detecção já iniciada.")

        parent_pipe, child_pipe = Pipe()
        detection_process = Process(target=start_detection, args=(child_pipe,))
        detection_process.start()

        asyncio.run(listen_pipe(detection_process, parent_pipe))

        return {"status": "ok", "code": 200, "detail": "Detecção iniciada."}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Iniciar a detecção falhou.")


@app.get("/stop-detection")
def get_stop_detection():
    try:
        global detection_process
        if detection_process is None:
            raise HTTPException(
                status_code=400, detail="Detecção não está em andamento."
            )

        detection_process.terminate()
        detection_process.join()
        detection_process = None

        return {"status": "ok", "code": 200, "detail": "Detecção encerrada."}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha na requisição.")


@app.get("/detections")
def get_all_detections():
    try:
        return crud.get_all_detection_records()
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha ao buscar detecções.")


@app.get("/detections/{id}")
def get_detection(id: int):
    try:
        return crud.get_detection_record(id)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha ao buscar detecção.")


@app.delete("/detections/{id}")
def delete_detection(id: int):
    try:
        crud.delete_detection_record(id)
        return {"success": True}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Falha ao apagar detecção.")


@app.get("/detections/{id}/raios")
def get_detection(id: int, request: Request):
    return templates.TemplateResponse("detections.html", {"request": request})


@app.get("/detections/{id}/lightnings")
def get_detection(id: int):
    try:
        return crud.get_lightnings_by_detection_id(id)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500, detail="Falha ao buscar raios da detecção."
        )


@app.websocket("/ws-connect/")
async def ws_connect(websocket: WebSocket):
    await ws.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("ws message:", data)
    except WebSocketDisconnect:
        ws.disconnect(websocket)
