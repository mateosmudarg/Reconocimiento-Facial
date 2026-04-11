import json

def read_config(prop):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config.get(prop)
    except Exception as e:
        raise Exception(f"Error al leer el archivo de configuración: {str(e)}")