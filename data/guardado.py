import os
from data.db import agregar_usuario, agregar_movimiento

def leer_imagen(path):
    if not os.path.exists(path):
        raise FileNotFoundError("La imagen no existe")
    
    with open(path, 'rb') as f:
        return f.read()

def guardar_reconocimiento_facial(image_path, name):
    if not name:
        raise ValueError("El nombre no puede estar vacío")

    img_data = leer_imagen(image_path)
    agregar_usuario(name, img_data)

def guardar_movimiento(id_usuario, fecha, img_movimiento, tipo):
    if not id_usuario:
        raise ValueError("ID de usuario inválido")

    img_data = leer_imagen(img_movimiento)
    agregar_movimiento(id_usuario, fecha, img_data, tipo)