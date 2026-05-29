from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)


class EnrollDialog(QDialog):
    """Formulario para registrar un nuevo empleado con el rostro capturado."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Registrar empleado")
        self.setMinimumWidth(360)

        self.nombre = QLineEdit()
        self.documento = QLineEdit()
        self.email = QLineEdit()
        self.departamento = QLineEdit()

        form = QFormLayout(self)
        form.addRow("Nombre *", self.nombre)
        form.addRow("Documento", self.documento)
        form.addRow("Email", self.email)
        form.addRow("Área", self.departamento)

        botones = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        botones.accepted.connect(self._validar)
        botones.rejected.connect(self.reject)
        form.addRow(botones)

    def _validar(self) -> None:
        if self.nombre.text().strip():
            self.accept()

    def datos(self) -> dict:
        return {
            "nombre": self.nombre.text().strip(),
            "documento": self.documento.text().strip() or None,
            "email": self.email.text().strip() or None,
            "departamento": self.departamento.text().strip() or None,
        }
