import os
from data.db import agregar_usuario, agregar_movimiento

def leer_imagen(path):
    if not path or not isinstance(path, str):
        return None
    if "\x00" in path:
        return None
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return f.read()

def guardar_reconocimiento_facial(image_path, name):
    if not name:
        raise ValueError("El nombre no puede estar vacío")

    img_data = leer_imagen(image_path)
    if not img_data:
        raise ValueError("Imagen inválida")

    agregar_usuario(name, img_data)

def guardar_movimiento(id_usuario, fecha, img_movimiento, tipo):
    if not id_usuario:
        raise ValueError("ID de usuario inválido")

    img_data = leer_imagen(img_movimiento)
    if not img_data:
        raise ValueError("Imagen inválida")

    agregar_movimiento(id_usuario, fecha, img_data, tipo)