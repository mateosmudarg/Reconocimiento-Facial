import tkinter as tk
from tkinter import messagebox
from data.db_init import init_db
from gui.ventana_principal import crear_ui, configurar_estilos

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Reconocimiento Facial")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

    def setup(self):
        try:
            db_creada = init_db()
            if db_creada:
                self.root.after(100, lambda: messagebox.showinfo(
                    "Bienvenido",
                    "Base de datos creada correctamente."
                ))
        except Exception as e:
            messagebox.showerror("Error crítico", str(e))
            return False

        configurar_estilos()
        crear_ui(self.root)

        return True

    def run(self):
        if self.setup():
            self.root.mainloop()