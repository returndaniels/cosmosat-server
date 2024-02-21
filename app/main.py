from fastapi import Request

from app import app, templates
from api import crud


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/camera-status")
def get_cam_status():
    return {"status": "enabled"}


@app.get("/detections")
def get_all_detections():
    return crud.get_all_detection_records()


@app.get("/detections/{id}")
def get_detection(id: int):
    return crud.get_detection_record(id)


@app.delete("/detections/{id}")
def delete_detection(id: int):
    crud.delete_detection_record(id)
    return {"success": True}
