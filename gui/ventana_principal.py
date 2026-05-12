from tkinter import ttk
from gui import movimientos, lista_usuarios, handlers
import core.arduino

def configurar_estilos():
    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 11), padding=6)
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))


def crear_boton(parent, text, command):
    btn = ttk.Button(parent, text=text, command=command)
    btn.pack(fill="x", pady=5)


def crear_ui(root):
    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)

    title = ttk.Label(frame, text="Gestión de Usuarios", style="Title.TLabel")
    title.pack(pady=(0, 15))

    crear_boton(frame, "Nuevo usuario", handlers.on_nuevo_usuario)
    crear_boton(frame, "Lista de usuarios", lambda: lista_usuarios.lista_usuarios(root))
    crear_boton(frame, "Validar entrada", lambda: handlers.on_agregar_movimiento("Entrada"))
    #crear_boton(frame, "Validar entrada", lambda: core.arduino.entrada())
    crear_boton(frame, "Validar salida", lambda: handlers.on_agregar_movimiento("Salida"))
    crear_boton(frame, "Lista de Movimientos", lambda: movimientos.mostrar_movimientos(root))