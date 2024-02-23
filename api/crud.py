from db import get_db


def create_detection_record(start_time):
    """
    Cria um novo registro de detecção na tabela "detection_records".

    Args:
        start_time (int): Timestamp de início da detecção (em segundos desde epoch).

    Returns:
        O ID do registro criado.
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO detection_records (start_time) VALUES (?)", (start_time,)
    )
    db.commit()

    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid


def create_lightning(timestamp, size, centroid_x, centroid_y, detection_id):
    """
    Insere um novo registro de relâmpago na tabela "lightnings".

    Args:
        timestamp (int): Timestamp do relâmpago (em segundos desde epoch).
        size (float): Tamanho estimado do relâmpago.
        centroid_x (float): Coordenada X do centroide do relâmpago.
        centroid_y (float): Coordenada Y do centroide do relâmpago.
        detection_id (int): ID da detecção associada ao relâmpago.
    """

    db = get_db()
    cursor = db.cursor()

    db.execute(
        "INSERT INTO lightnings (timestamp, size, centroid_x, centroid_y, detection_id) VALUES (?, ?, ?, ?, ?)",
        (
            timestamp,
            size,
            centroid_x,
            centroid_y,
            detection_id,
        ),
    )
    db.commit()
    return cursor.lastrowid


def get_all_detection_records():
    """
    Obtém todos os registros de detecção da tabela "detection_records".

    Returns:
        list: Lista de registros de detecção.
    """

    db = get_db()
    return db.execute("SELECT * FROM detection_records").fetchall()


def get_detection_record(id):
    """
    Obtém um registro de detecção específico da tabela "detection_records" com base no ID.

    Args:
        id (int): ID do registro de detecção a ser recuperado.

    Returns:
        tuple or None: Tupla representando o registro de detecção ou None se não for encontrado.
    """

    db = get_db()
    return db.execute("SELECT * FROM detection_records WHERE id = ?", (id,)).fetchone()


def delete_detection_record(id):
    """
    Exclui um registro de detecção específico da tabela "detection_records" com base no ID,
    e também exclui todas as lightnings que possuem o `detection_id` associado.

    Args:
        id (int): ID do registro de detecção a ser excluído.
    """

    db = get_db()

    # Deleta as lightnings associadas ao detection_id
    cursor = db.cursor()
    cursor.execute("DELETE FROM lightnings WHERE detection_id = ?", (id,))
    cursor.close()

    # Deleta o registro de detecção
    db.execute("DELETE FROM detection_records WHERE id = ?", (id,))
    db.commit()


def get_lightnings_by_detection_id(detection_id):
    """
    Busca todos os registros de relâmpagos na tabela "lightnings" que possuem um `detection_id` específico.

    Args:
      detection_id (int): ID da detecção a ser utilizada como filtro.

    Returns:
      list: Lista de registros de relâmpagos.
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM lightnings WHERE detection_id = ?", (detection_id,))
    lightnings = cursor.fetchall()
    cursor.close()
    return lightnings


def get_lightning_by_id(id):
    """
    Obtém um registro de relâmpago específico da tabela "lightnings" com base no ID.

    Args:
        id (int): ID do registro de relâmpago a ser recuperado.

    Returns:
        tuple or None: Tupla representando o registro de relâmpago ou None se não for encontrado.
    """

    db = get_db()
    return db.execute("SELECT * FROM lightnings WHERE id = ?", (id,)).fetchone()
