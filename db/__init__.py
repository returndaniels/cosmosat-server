import sqlite3


def create_db():
    """
    Cria e configura o banco de dados SQLite para armazenar informações sobre relâmpagos e detecções.

    Returns:
        sqlite3.Connection: Conexão com o banco de dados recém-criado.
    """

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
    """
    Obtém a conexão com o banco de dados SQLite para ser usada em operações de leitura/gravação.

    Returns:
        sqlite3.Connection: Conexão com o banco de dados.
    """

    db = sqlite3.connect("detections.db")
    db.row_factory = sqlite3.Row
    return db


# Criando uma instância do banco de dados e fechando-a imediatamente para evitar vazamentos.
db = create_db()
db.close()
