import sys
import os

from PyQt5.QtWidgets import QApplication, QMessageBox

from data.db_init import init_db
from gui.ventana_principal import VentanaPrincipal, configurar_estilos
from gui.configuracion import setup_config


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None

    def setup(self):
        try:
            if not os.path.exists("config.json"):
                # IMPORTANTE: ahora deberías adaptar setup_config a PyQt
                setup_config()

            init_db()

        except Exception as e:
            QMessageBox.critical(None, "Error crítico", str(e))
            return False

        configurar_estilos(self.app)

        self.window = VentanaPrincipal()
        return True

    def run(self):
        if self.setup():
            self.window.show()
            sys.exit(self.app.exec_())