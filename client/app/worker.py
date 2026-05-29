"""Worker de inferencia facial ejecutado en un hilo aparte para no bloquear la UI."""

import base64

import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot

from .api_client import ApiClient, ApiError
from .face_engine import FaceEngine


def _jpeg_b64(frame_bgr: np.ndarray, max_w: int = 480) -> str:
    h, w = frame_bgr.shape[:2]
    if w > max_w:
        frame_bgr = cv2.resize(frame_bgr, (max_w, int(h * max_w / w)))
    ok, buf = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return base64.b64encode(buf).decode() if ok else ""


class InferenceWorker(QObject):
    preview_ready = Signal(list)        # lista de bboxes (x1,y1,x2,y2)
    recognized = Signal(dict)           # respuesta del servidor
    enrolled = Signal(object, object)   # (embedding|None, foto_b64|None)
    failed = Signal(str)

    def __init__(self, api: ApiClient, engine: FaceEngine, device: str) -> None:
        super().__init__()
        self._api = api
        self._engine = engine
        self._device = device
        self._busy = False

    @Slot(object)
    def do_preview(self, frame: np.ndarray) -> None:
        if self._busy:
            return
        self._busy = True
        try:
            caras = self._engine.detect(frame)
            self.preview_ready.emit([c.bbox for c in caras])
        except Exception:
            self.preview_ready.emit([])
        finally:
            self._busy = False

    @Slot(object, str)
    def do_action(self, frame: np.ndarray, tipo: str) -> None:
        try:
            cara = self._engine.rostro_principal(frame)
            if cara is None:
                self.failed.emit("No se detectó ningún rostro")
                return
            resp = self._api.identificar(
                embedding=cara.embedding.tolist(),
                tipo=tipo,
                dispositivo=self._device,
                imagen_b64=_jpeg_b64(frame),
            )
            self.recognized.emit(resp)
        except ApiError as e:
            self.failed.emit(str(e))
        except Exception as e:
            self.failed.emit(f"Error: {e}")

    @Slot(object)
    def do_enroll(self, frame: np.ndarray) -> None:
        try:
            cara = self._engine.rostro_principal(frame)
            if cara is None:
                self.enrolled.emit(None, None)
                return
            self.enrolled.emit(cara.embedding.tolist(), _jpeg_b64(frame, max_w=240))
        except Exception as e:
            self.failed.emit(f"Error: {e}")
