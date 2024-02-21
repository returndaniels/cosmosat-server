from fastapi import Request, HTTPException

from api import crud
from app import app, templates
from db.models import DetectionRecord
from typing import List


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/camera-status")
def get_cam_status():
    return {"status": "enabled"}


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
