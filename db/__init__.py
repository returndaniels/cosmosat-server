import sqlite3


def create_db():
    db = sqlite3.connect("detections.db")
    db.execute(
        """CREATE TABLE IF NOT EXISTS lightnings (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     detection_id INTEGER REFERENCES detection_records(id),
                     timestamp INTEGER,
                     size INTEGER,
                     centroid_x REAL,
                     centroid_y REAL
                 )"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS detection_records (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     start_time INTEGER
                 )"""
    )
    db.commit()
    return db


def get_db():
    db = sqlite3.connect("detections.db")
    db.row_factory = sqlite3.Row
    return db


db = create_db()
db.close()
