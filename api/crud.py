from db import get_db


def create_detection_record(start_time):
    db = get_db()
    db.execute("INSERT INTO detection_records (start_time) VALUES (?)", (start_time,))
    db.commit()


def get_all_detection_records():
    db = get_db()
    return db.execute("SELECT * FROM detection_records").fetchall()


def get_detection_record(id):
    db = get_db()
    return db.execute("SELECT * FROM detection_records WHERE id = ?", (id,)).fetchone()


def delete_detection_record(id):
    db = get_db()
    db.execute("DELETE FROM detection_records WHERE id = ?", (id,))
    db.commit()
