import sqlite3
from data.read_config import read_config

DB_NAME = read_config("database")["name"]

def ejecutar(query, params=None, fetchone=False, fetchall=False):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Error en base de datos: {e}")

def agregar_usuario(nombre, imagen):
    query = """
        INSERT INTO usuarios (fecha, nombre, imagen)
        VALUES (strftime('%Y-%m-%d', 'now', 'localtime'), ?, ?)
    """
    return ejecutar(query, (nombre, imagen))

def obtener_usuarios(asc=True, limit=10):
    order = "ASC" if asc else "DESC"
    if limit == 0:
        query = f"""
            SELECT id, fecha, nombre, imagen
            FROM usuarios
            ORDER BY id {order}
        """
        return ejecutar(query, fetchall=True)

    query = f"""
        SELECT id, fecha, nombre, imagen
        FROM usuarios
        ORDER BY id {order}
        LIMIT ?
    """
    return ejecutar(query, (limit,), fetchall=True)

def agregar_movimiento(id_usuario, fecha, imagen, tipo):
    query = """
        INSERT INTO movimientos (fk_id_usuarios, fecha, imagen, tipo)
        VALUES (?, ?, ?, ?)
    """
    return ejecutar(query, (id_usuario, fecha, imagen, tipo))

def obtener_movimientos(limit=10):
    if limit == 0:
        query = """
            SELECT id, fk_id_usuarios, fecha, imagen, tipo
            FROM movimientos
            ORDER BY id DESC
        """
        return ejecutar(query, fetchall=True)
    query = """
        SELECT id, fk_id_usuarios, fecha, imagen, tipo
        FROM movimientos
        ORDER BY id DESC
        LIMIT ?
    """
    return ejecutar(query, (limit,), fetchall=True)

def eliminar_usuarios_por_ids(ids):
    if not ids:
        return False
    placeholders = ",".join("?" for _ in ids)
    query = f"DELETE FROM usuarios WHERE id IN ({placeholders})"
    ejecutar(query, ids)
    return True