import sqlite3

def get_db():
    db = sqlite3.connect("detections.db")
    db.row_factory = sqlite3.Row
    return db
