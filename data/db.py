import sqlite3

def connect(query, params=None, fetchone=False, fetchall=False):
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()

        conn.commit()
        conn.close()

        return result

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None


def agregar_usuario(nombre, imagen):
    return connect(
        "INSERT INTO usuarios (fecha, nombre, imagen) VALUES (strftime('%Y-%m-%d', 'now', 'localtime'), ?, ?)",
        (nombre, imagen)
    )


def obtener_usuarios(asc=True, limit=10):
    order = "ASC" if asc else "DESC"

    if limit == 0:
        query = f"SELECT id, fecha, nombre, imagen FROM usuarios ORDER BY id {order}"
        return connect(query, fetchall=True)
    else:
        query = f"SELECT id, fecha, nombre, imagen FROM usuarios ORDER BY id {order} LIMIT ?"
        return connect(query, (limit,), fetchall=True)


def agregar_movimiento(id_usuario, fecha, imagen, tipo):
    return connect(
        "INSERT INTO movimientos (fk_id_usuarios, fecha, imagen, tipo) VALUES (?, ?, ?, ?)",
        (id_usuario, fecha, imagen, tipo)
    )

def obtener_movimientos(limit=10):
    if limit == 0:
        query = "SELECT id, fk_id_usuarios, fecha, imagen, tipo FROM movimientos ORDER BY id DESC"
        return connect(query, fetchall=True)
    else:
        query = "SELECT id, fk_id_usuarios, fecha, imagen, tipo FROM movimientos ORDER BY id DESC LIMIT ?"
        return connect(query, (limit,), fetchall=True)
    
def eliminar_usuarios_por_ids(ids):
    if not ids:
        return False
    placeholders = ",".join("?" for _ in ids)
    query = f"DELETE FROM usuarios WHERE id IN ({placeholders})"
    connect(query, ids)
    return True