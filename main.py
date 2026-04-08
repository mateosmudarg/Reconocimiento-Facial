import io
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from core import gestion_movimientos
import core.reconocimiento as reconocimiento
from gui import movimientos, lista_usuarios
from data.db import obtener_usuarios


root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")
root.geometry("400x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

title = ttk.Label(main_frame, text="Gestión de Usuarios", style="Title.TLabel")
title.pack(pady=(0, 15))

ttk.Button(
    main_frame,
    text="Nuevo usuario",
    command=reconocimiento.empezar_reconocimiento_facial,
).pack(fill="x", pady=5)

ttk.Button(
    main_frame,
    text="Lista de usuarios",
    command=lambda: lista_usuarios.lista_usuarios(root)
).pack(fill="x", pady=5)

ttk.Button(
    main_frame,
    text="Validar entrada",
    command=lambda: gestion_movimientos.facial("Entrada"),
).pack(fill="x", pady=5)

ttk.Button(
    main_frame,
    text="Validar salida",
    command=lambda: gestion_movimientos.facial("Salida"),
).pack(fill="x", pady=5)

ttk.Button(
    main_frame,
    text="Lista de Movimientos",
    command=lambda: movimientos.mostrar_movimientos(root),
).pack(fill="x", pady=5)

root.mainloop()