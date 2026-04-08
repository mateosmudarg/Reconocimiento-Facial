from tkinter import messagebox
import sqlite3
from data.db import agregar_usuario, agregar_movimiento

def guardar_reconocimiento_facial(image_path, name):
    try:
        with open(image_path, 'rb') as image_file:
            img_data = image_file.read()
        agregar_usuario(name, img_data)
        messagebox.showinfo("Éxito", "Reconocimiento e imagen guardados exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    
def guardar_movimiento(id_usuario, fecha, img_movimiento, tipo):
    try:
        with open(img_movimiento, 'rb') as image_file:
            img_data = image_file.read()
        agregar_movimiento(id_usuario, fecha, img_data, tipo)
        messagebox.showinfo("Éxito", "Movimiento e imagen guardados exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")