import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal


class CameraThread(QThread):
    """Captura frames de la cámara en un hilo dedicado y los emite."""

    frame_ready = Signal(np.ndarray)
    error = Signal(str)

    def __init__(self, index: int = 0) -> None:
        super().__init__()
        self._index = index
        self._running = False
        self._last: np.ndarray | None = None

    def run(self) -> None:
        cap = cv2.VideoCapture(self._index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(self._index)
        if not cap.isOpened():
            self.error.emit("No se pudo abrir la cámara.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self._running = True
        while self._running:
            ok, frame = cap.read()
            if not ok:
                continue
            self._last = frame
            self.frame_ready.emit(frame)
            self.msleep(20)
        cap.release()

    def snapshot(self) -> np.ndarray | None:
        return None if self._last is None else self._last.copy()

    def stop(self) -> None:
        self._running = False
        self.wait(1500)
