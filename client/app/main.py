import sys

from PySide6.QtWidgets import QApplication, QStackedWidget

from .ui.login_window import LoginWindow
from .ui.main_window import MainWindow
from .ui.theme import QSS


class RecFacApp(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RecFac · Control de Accesos")
        self.resize(960, 720)

        self.login = LoginWindow()
        self.login.logged_in.connect(self._on_login)
        self.addWidget(self.login)

    def _on_login(self, api, data) -> None:
        main = MainWindow(api, data)
        self.addWidget(main)
        self.setCurrentWidget(main)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    win = RecFacApp()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
