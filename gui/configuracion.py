import json
import tkinter as tk
from tkinter import ttk
from .dialogs import exito, advertencia, confirmar, mostrar_excepcion


class ConfigWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Configuración")
        self.resizable(False, False)

        self.transient(root)
        self.grab_set()

        self.config_data = {"database": {}}

        self._build_ui()
        self._center(root)

    def _center(self, root):
        self.update_idletasks()

        w = 300
        h = 300

        x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Base de datos").pack(anchor="w")

        self.db_type = ttk.Combobox(
            frame, values=["sqlite", "mysql"], state="readonly", height=2
        )
        self.db_type.pack(fill="x", pady=(0, 10))
        self.db_type.bind("<<ComboboxSelected>>", self._render_fields)

        self.fields_frame = ttk.Frame(frame)
        self.fields_frame.pack(fill="both", expand=True)

        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=(10, 0))

        ttk.Button(btns, text="Cancelar", command=self._cancel).pack(side="right")
        ttk.Button(btns, text="Guardar", command=self._save).pack(side="right", padx=5)

    def _clear_fields(self):
        for w in self.fields_frame.winfo_children():
            w.destroy()

    def _render_fields(self, event=None):
        self._clear_fields()
        self.inputs = {}

        db_type = self.db_type.get()

        if db_type == "sqlite":
            ttk.Label(self.fields_frame, text="Archivo:").pack(anchor="w")
            entry = ttk.Entry(self.fields_frame)
            entry.pack(fill="x", pady=5)
            self.inputs["nombre"] = entry

        elif db_type == "mysql":
            for label, key, show in [
                ("Host", "host", None),
                ("Usuario", "user", None),
                ("Contraseña", "password", "*"),
                ("DB", "db", None),
            ]:
                ttk.Label(self.fields_frame, text=label + ":").pack(anchor="w")
                e = ttk.Entry(self.fields_frame, show=show)
                e.pack(fill="x", pady=2)
                self.inputs[key] = e

    def _validate(self):
        for k, e in self.inputs.items():
            if not e.get().strip():
                advertencia(f"Completar: {k}")
                return False
        return True

    def _save(self):
        try:
            if not self._validate():
                return

            db_type = self.db_type.get()

            if db_type == "sqlite":
                nombre = self.inputs["nombre"].get().strip()
                if not nombre.endswith(".db"):
                    nombre += ".db"

                self.config_data["database"]["url"] = f"sqlite:///{nombre}"

            elif db_type == "mysql":
                host = self.inputs["host"].get().strip()
                user = self.inputs["user"].get().strip()
                password = self.inputs["password"].get().strip()
                db = self.inputs["db"].get().strip()

                self.config_data["database"][
                    "url"
                ] = f"mysql+pymysql://{user}:{password}@{host}:3306/{db}"

            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4)

            exito("Configuración guardada")
            self.destroy()

        except Exception as e:
            mostrar_excepcion(e)

    def _cancel(self):
        if confirmar("¿Cancelar configuración?"):
            self.destroy()


def setup_config(root):
    win = ConfigWindow(root)
    root.wait_window(win)
