import sqlite3
import os
from data.read_config import read_config
DB_NAME = read_config("database")["name"]

def init_db(db_name: str = DB_NAME) -> bool:
    db_exists = os.path.exists(db_name)

    create_usuarios_table = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        nombre TEXT NOT NULL,
        imagen BLOB
    );
    """

    create_movimientos_table = """
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_id_usuarios INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        imagen BLOB,
        tipo TEXT NOT NULL,
        FOREIGN KEY (fk_id_usuarios) REFERENCES usuarios(id) ON DELETE CASCADE
    );
    """

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(create_usuarios_table)
            cursor.execute(create_movimientos_table)
            conn.commit()

        return not db_exists

    except sqlite3.Error as e:
        raise RuntimeError(f"Error de base de datos: {e}")