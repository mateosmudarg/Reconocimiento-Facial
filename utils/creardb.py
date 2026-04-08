import sqlite3
from tkinter import messagebox
def create_table():
     try:
         conn = sqlite3.connect('reconocimientos.db')
         cursor = conn.cursor()
         cursor.execute('''
         CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                fecha TEXT,
                nombre TEXT,
                imagen BLOB
         )
                        ''')
         cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY,
                fk_id_usuarios INTEGER,
                fecha TEXT,
                imagen BLOB,
                tipo TEXT,
                FOREIGN KEY (fk_id_usuarios) REFERENCES usuarios(id)
            )
                        ''')
         conn.commit()
         conn.close()
         messagebox.showinfo("Éxito", "Tabla creada correctamente.")
     except Exception as e:
         messagebox.showerror("Error", f"Ocurrió un error al crear la tabla: {e}") 

create_table()