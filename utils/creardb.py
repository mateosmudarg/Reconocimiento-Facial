import sqlite3
from tkinter import messagebox

DB_NAME = "reconocimientos.db"

def create_tables(db_name: str = DB_NAME) -> None:

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
        messagebox.showinfo("Éxito", "Tablas creadas correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudieron crear las tablas: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    create_tables()