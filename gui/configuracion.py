import json
from tkinter import simpledialog
from .dialogs import info, exito, advertencia, error, confirmar, mostrar_excepcion


def _ask_required_string(root, title, prompt, show=None):
    while True:
        value = simpledialog.askstring(title, prompt, parent=root, show=show)

        if value is None:
            if confirmar("¿Cancelar configuración?"):
                raise Exception("Configuración cancelada")
            continue

        value = value.strip()

        if not value:
            advertencia("Este campo es obligatorio")
            continue

        return value


def _select_db_type(root):
    while True:
        db_type = simpledialog.askstring(
            "Base de datos",
            "Tipo de base de datos (sqlite/mysql):",
            parent=root
        )

        if db_type is None:
            if confirmar("¿Cancelar configuración?"):
                raise Exception("Configuración cancelada")
            continue

        db_type = db_type.lower().strip()

        if db_type in ("sqlite", "mysql"):
            return db_type

        error("Tipo inválido. Usa 'sqlite' o 'mysql'")


def setup_config(root):
    try:
        info("Configura la base de datos")

        config = {"database": {}}
        db_type = _select_db_type(root)

        if db_type == "sqlite":
            nombre = _ask_required_string(
                root,
                "SQLite",
                "Nombre del archivo (ej: reconocimientos.db):"
            )

            if not nombre.endswith(".db"):
                nombre += ".db"

            config["database"]["url"] = f"sqlite:///{nombre}"

        elif db_type == "mysql":
            host = _ask_required_string(root, "MySQL", "Host:")
            user = _ask_required_string(root, "MySQL", "Usuario:")
            password = _ask_required_string(root, "MySQL", "Contraseña:", show="*")
            db = _ask_required_string(root, "MySQL", "Nombre de la base:")

            port = simpledialog.askstring(
                "MySQL",
                "Puerto (default 3306):",
                parent=root
            )
            port = port.strip() if port else "3306"

            config["database"]["url"] = (
                f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
            )

        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

        except Exception as e:
            raise Exception(f"No se pudo guardar config.json: {e}")

        exito("Configuración guardada correctamente")

    except Exception as e:
        if str(e) == "Configuración cancelada":
            advertencia("Configuración cancelada por el usuario")
        else:
            mostrar_excepcion(e)