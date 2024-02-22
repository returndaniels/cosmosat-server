from fastapi import Request, HTTPException, WebSocket

from api import crud
from api.main import start_detection, stop_detection
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
    if start_detection() == 200:
        return {"status": "ok", "code": 200, "detail": "Detecção iniciada"}
    else:
        raise HTTPException(status_code=500, detail=str("Falha na requisição"))


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


@app.websocket("/raios/")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ws.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await ws.send_personal_message(f"You wrote: {data}", websocket)
        await ws.broadcast(f"Client #{client_id} says: {data}")
