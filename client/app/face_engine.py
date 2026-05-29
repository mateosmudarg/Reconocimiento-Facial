"""Motor de reconocimiento facial moderno basado en InsightFace (ArcFace).

Reemplaza el enfoque anterior (Haar Cascade + diferencia de píxeles) por
detección robusta y embeddings de 512 dimensiones, que ofrecen mayor
precisión, tolerancia a iluminación/ángulos y soporte multi-rostro.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class DetectedFace:
    bbox: tuple[int, int, int, int]  # x1, y1, x2, y2
    embedding: np.ndarray
    score: float


class FaceEngine:
    def __init__(self, model_name: str, provider: str) -> None:
        self._model_name = model_name
        self._provider = provider
        self._app = None  # carga perezosa (la inicialización descarga modelos)

    def _ensure_loaded(self) -> None:
        if self._app is not None:
            return
        try:
            from insightface.app import FaceAnalysis
        except ImportError as e:  # pragma: no cover
            raise RuntimeError(
                "InsightFace no está instalado. Ejecute: pip install -r requirements.txt"
            ) from e

        app = FaceAnalysis(name=self._model_name, providers=[self._provider])
        app.prepare(ctx_id=0, det_size=(640, 640))
        self._app = app

    def detect(self, frame_bgr: np.ndarray) -> list[DetectedFace]:
        """Detecta todos los rostros del frame con sus embeddings."""
        self._ensure_loaded()
        caras = self._app.get(frame_bgr)
        resultado: list[DetectedFace] = []
        for c in caras:
            x1, y1, x2, y2 = (int(v) for v in c.bbox)
            resultado.append(
                DetectedFace(
                    bbox=(x1, y1, x2, y2),
                    embedding=c.normed_embedding.astype(np.float32),
                    score=float(c.det_score),
                )
            )
        return resultado

    def rostro_principal(self, frame_bgr: np.ndarray) -> DetectedFace | None:
        """Devuelve el rostro más grande (el más cercano a la cámara)."""
        caras = self.detect(frame_bgr)
        if not caras:
            return None
        return max(
            caras,
            key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
        )
