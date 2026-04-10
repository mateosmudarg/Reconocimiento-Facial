import tkinter as tk
from tkinter import messagebox, ttk
from data.db_init import init_db
from gui import movimientos, lista_usuarios
from gui import handlers

def main():
    try:
        db_creada = init_db()
    except Exception as e:
        messagebox.showerror("Error crítico", str(e))
        return

    root = tk.Tk()
    root.title("Sistema de Reconocimiento Facial")
    root.geometry("400x400")
    root.resizable(False, False)

    if db_creada:
        root.after(100, lambda: messagebox.showinfo(
            "Bienvenido",
            "Base de datos creada correctamente."
        ))

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
        command=lambda: handlers.on_nuevo_usuario(),
    ).pack(fill="x", pady=5)

    ttk.Button(
        main_frame,
        text="Lista de usuarios",
        command=lambda: lista_usuarios.lista_usuarios(root)
    ).pack(fill="x", pady=5)

    ttk.Button(
        main_frame,
        text="Validar entrada",
        command=lambda: handlers.on_agregar_movimiento("Entrada"),
    ).pack(fill="x", pady=5)

    ttk.Button(
        main_frame,
        text="Validar salida",
        command=lambda: handlers.on_agregar_movimiento("Salida"),
    ).pack(fill="x", pady=5)

    ttk.Button(
        main_frame,
        text="Lista de Movimientos",
        command=lambda: movimientos.mostrar_movimientos(root),
    ).pack(fill="x", pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()