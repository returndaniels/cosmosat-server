from api.database import get_db

def create_detection_record(start_time):
    db = get_db()
    db.execute("INSERT INTO detections (start_time) VALUES (?)", (start_time,))
    db.commit()

def get_all_detection_records():
    db = get_db()
    return db.execute("SELECT * FROM detections").fetchall()

def get_detection_record(id):
    db = get_db()
    return db.execute("SELECT * FROM detections WHERE id = ?", (id,)).fetchone()

def delete_detection_record(id):
    db = get_db()
    db.execute("DELETE FROM detections WHERE id = ?", (id,))
    db.commit()
