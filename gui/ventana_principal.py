from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

from gui import movimientos, lista_usuarios, handlers


def configurar_estilos(app):
    app.setStyleSheet(
        """
        QPushButton {
            font-family: Segoe UI;
            font-size: 11pt;
            padding: 6px;
        }
        QLabel#title {
            font-family: Segoe UI;
            font-size: 16pt;
            font-weight: bold;
        }
    """
    )

def crear_boton(text, callback):
    btn = QPushButton(text)
    btn.clicked.connect(callback)
    return btn

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reconocimiento Facial")
        self.setGeometry(100, 100, 400, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        title = QLabel("Gestión de Usuarios")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        layout.addWidget(crear_boton("Nuevo usuario", handlers.on_nuevo_usuario))

        layout.addWidget(
            crear_boton(
                "Lista de usuarios", lambda: lista_usuarios.lista_usuarios(self)
            )
        )

        layout.addWidget(
            crear_boton(
                "Validar entrada", lambda: handlers.on_agregar_movimiento("Entrada")
            )
        )

        layout.addWidget(
            crear_boton(
                "Validar salida", lambda: handlers.on_agregar_movimiento("Salida")
            )
        )

        layout.addWidget(
            crear_boton(
                "Lista de Movimientos", lambda: movimientos.mostrar_movimientos(self)
            )
        )

        self.setLayout(layout)
