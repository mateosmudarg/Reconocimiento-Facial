import json
from tkinter import simpledialog, messagebox

def setup_config(root):
    messagebox.showinfo("Configuración inicial", "Configura la base de datos")

    db_type = simpledialog.askstring(
        "Base de datos",
        "Tipo de base de datos (sqlite/mysql):",
        parent=root
    )

    if not db_type:
        raise Exception("Configuración cancelada")

    db_type = db_type.lower()

    config = {"database": {}}

    if db_type == "sqlite":
        nombre = simpledialog.askstring(
            "SQLite",
            "Nombre del archivo (ej: reconocimientos.db):",
            parent=root
        )

        config["database"]["url"] = f"sqlite:///{nombre}"

    elif db_type == "mysql":
        host = simpledialog.askstring("MySQL", "Host:", parent=root)
        user = simpledialog.askstring("MySQL", "Usuario:", parent=root)
        password = simpledialog.askstring("MySQL", "Contraseña:", parent=root, show="*")
        db = simpledialog.askstring("MySQL", "Nombre de la base:", parent=root)

        config["database"]["url"] = f"mysql+pymysql://{user}:{password}@{host}/{db}"

    else:
        raise Exception("Tipo de base de datos no soportado")

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    messagebox.showinfo("Listo", "Configuración guardada correctamente")