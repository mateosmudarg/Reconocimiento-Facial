import tkinter as tk
from tkinter import messagebox
from data.db_init import init_db
from gui.ventana_principal import crear_ui, configurar_estilos
from gui.configuracion import setup_config

import os
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Reconocimiento Facial")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

    def setup(self):
        try:
            if not os.path.exists("config.json"):
                setup_config(self.root)

            from data.db_init import init_db
            init_db()

        except Exception as e:
            messagebox.showerror("Error crítico", str(e))
            return False

        configurar_estilos()
        crear_ui(self.root)

        return True

    def run(self):
        if self.setup():
            self.root.mainloop()