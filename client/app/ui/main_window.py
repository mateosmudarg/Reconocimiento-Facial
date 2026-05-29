import cv2
import numpy as np
from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..api_client import ApiClient, ApiError
from ..arduino_serial import ArduinoDoor
from ..camera import CameraThread
from ..config import settings
from ..face_engine import FaceEngine
from ..worker import InferenceWorker
from .enroll_dialog import EnrollDialog


def frame_a_pixmap(frame_bgr: np.ndarray, boxes: list, ancho: int) -> QPixmap:
    img = frame_bgr.copy()
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(img, (x1, y1), (x2, y2), (129, 140, 248), 2)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg).scaledToWidth(
        ancho, Qt.SmoothTransformation
    )


class MainWindow(QWidget):
    request_preview = Signal(object)
    request_action = Signal(object, str)
    request_enroll = Signal(object)

    def __init__(self, api: ApiClient, login_data: dict) -> None:
        super().__init__()
        self.setObjectName("root")
        self._api = api
        self._role = login_data.get("role", "operator")
        self._boxes: list = []
        self._frame: np.ndarray | None = None

        self.arduino = ArduinoDoor(settings.arduino_port, settings.arduino_baud)

        self._build_ui(login_data)
        self._start_camera()
        self._start_worker()

    # ---------- UI ----------
    def _build_ui(self, login_data: dict) -> None:
        self.video = QLabel("Iniciando cámara…")
        self.video.setObjectName("video")
        self.video.setAlignment(Qt.AlignCenter)
        self.video.setMinimumSize(820, 500)

        self.status = QLabel(f"Listo · {settings.device_name}")
        self.status.setObjectName("status")
        self.status.setAlignment(Qt.AlignCenter)

        btn_entrada = QPushButton("✓  Registrar Entrada")
        btn_entrada.setObjectName("entrada")
        btn_entrada.clicked.connect(lambda: self._accion("entrada"))

        btn_salida = QPushButton("⏏  Registrar Salida")
        btn_salida.setObjectName("salida")
        btn_salida.clicked.connect(lambda: self._accion("salida"))

        acciones = QHBoxLayout()
        acciones.addWidget(btn_entrada)
        acciones.addWidget(btn_salida)

        barra = QHBoxLayout()
        titulo = QLabel(f"RecFac · {login_data.get('full_name', '')}")
        titulo.setObjectName("title")
        barra.addWidget(titulo)
        barra.addStretch()
        if self._role == "admin":
            btn_enroll = QPushButton("＋ Registrar empleado")
            btn_enroll.setObjectName("primary")
            btn_enroll.clicked.connect(self._enrolar)
            barra.addWidget(btn_enroll)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addLayout(barra)
        layout.addWidget(self.video, alignment=Qt.AlignCenter)
        layout.addWidget(self.status)
        layout.addLayout(acciones)

    # ---------- Cámara ----------
    def _start_camera(self) -> None:
        self.cam = CameraThread(settings.camera_index)
        self.cam.frame_ready.connect(self._on_frame)
        self.cam.error.connect(lambda m: self.status.setText(f"⚠ {m}"))
        self.cam.start()

        self.preview_timer = QTimer(self)
        self.preview_timer.setInterval(350)
        self.preview_timer.timeout.connect(self._tick_preview)
        self.preview_timer.start()

    def _on_frame(self, frame: np.ndarray) -> None:
        self._frame = frame
        self.video.setPixmap(frame_a_pixmap(frame, self._boxes, self.video.width()))

    def _tick_preview(self) -> None:
        if self._frame is not None:
            self.request_preview.emit(self._frame.copy())

    # ---------- Worker ----------
    def _start_worker(self) -> None:
        engine = FaceEngine(settings.face_model, settings.face_provider)
        self.thread = QThread(self)
        self.worker = InferenceWorker(self._api, engine, settings.device_name)
        self.worker.moveToThread(self.thread)

        self.request_preview.connect(self.worker.do_preview)
        self.request_action.connect(self.worker.do_action)
        self.request_enroll.connect(self.worker.do_enroll)
        self.worker.preview_ready.connect(self._on_preview)
        self.worker.recognized.connect(self._on_recognized)
        self.worker.enrolled.connect(self._on_enrolled)
        self.worker.failed.connect(self._on_failed)

        self.thread.start()

    def _on_preview(self, boxes: list) -> None:
        self._boxes = boxes

    # ---------- Acciones ----------
    def _accion(self, tipo: str) -> None:
        if self._frame is None:
            return
        self.status.setText("Procesando…")
        self.request_action.emit(self._frame.copy(), tipo)

    def _on_recognized(self, resp: dict) -> None:
        if resp.get("ok"):
            self.status.setStyleSheet("background:#16a34a")
            self.status.setText(
                f"✓ {resp['mensaje']}  ({resp['confianza']*100:.0f}%)"
            )
            if resp.get("tipo") == "entrada" and self.arduino.disponible:
                self.arduino.abrir_puerta()
        else:
            self.status.setStyleSheet("background:#b45309")
            self.status.setText(f"✗ {resp.get('mensaje', 'No reconocido')}")
        QTimer.singleShot(3500, self._reset_status)

    def _on_failed(self, msg: str) -> None:
        self.status.setStyleSheet("background:#b91c1c")
        self.status.setText(f"⚠ {msg}")
        QTimer.singleShot(3500, self._reset_status)

    def _reset_status(self) -> None:
        self.status.setStyleSheet("")
        self.status.setText(f"Listo · {settings.device_name}")

    # ---------- Enrolamiento ----------
    def _enrolar(self) -> None:
        if self._frame is not None:
            self.status.setText("Capturando rostro…")
            self.request_enroll.emit(self._frame.copy())

    def _on_enrolled(self, embedding, foto_b64) -> None:
        self._reset_status()
        if embedding is None:
            QMessageBox.warning(self, "Sin rostro", "No se detectó un rostro válido.")
            return
        dlg = EnrollDialog(self)
        if not dlg.exec():
            return
        payload = dlg.datos()
        payload["embedding"] = embedding
        payload["foto_b64"] = foto_b64
        try:
            emp = self._api.crear_empleado(payload)
            QMessageBox.information(
                self, "Empleado registrado", f"{emp['nombre']} creado correctamente."
            )
        except ApiError as e:
            QMessageBox.critical(self, "Error", str(e))

    # ---------- Cierre ----------
    def closeEvent(self, event) -> None:
        self.preview_timer.stop()
        self.cam.stop()
        self.thread.quit()
        self.thread.wait(1500)
        self.arduino.close()
        self._api.close()
        super().closeEvent(event)
