from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..api_client import ApiClient, ApiError
from ..config import settings


class LoginWindow(QWidget):
    logged_in = Signal(object, dict)  # (ApiClient, datos_login)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("root")

        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(380)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(8)

        logo = QLabel("RecFac")
        logo.setObjectName("logo")
        sub = QLabel("Cliente de control de accesos")
        sub.setObjectName("subtitle")

        self.url = QLineEdit(settings.server_url)
        self.url.setPlaceholderText("URL del servidor")
        self.user = QLineEdit()
        self.user.setPlaceholderText("Usuario")
        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Contraseña")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.returnPressed.connect(self._login)

        self.err = QLabel("")
        self.err.setObjectName("err")

        btn = QPushButton("Ingresar")
        btn.setObjectName("primary")
        btn.clicked.connect(self._login)

        layout.addWidget(logo)
        layout.addWidget(sub)
        layout.addSpacing(14)
        layout.addWidget(QLabel("Servidor"))
        layout.addWidget(self.url)
        layout.addWidget(QLabel("Usuario"))
        layout.addWidget(self.user)
        layout.addWidget(QLabel("Contraseña"))
        layout.addWidget(self.pwd)
        layout.addWidget(self.err)
        layout.addSpacing(8)
        layout.addWidget(btn)

        root = QVBoxLayout(self)
        root.addStretch()
        root.addWidget(card, alignment=Qt.AlignCenter)
        root.addStretch()

    def _login(self) -> None:
        self.err.setText("")
        api = ApiClient(self.url.text().strip() or settings.server_url)
        try:
            data = api.login(self.user.text().strip(), self.pwd.text())
        except ApiError as e:
            self.err.setText(str(e))
            return
        except Exception:
            self.err.setText("No se pudo conectar con el servidor")
            return
        self.logged_in.emit(api, data)
