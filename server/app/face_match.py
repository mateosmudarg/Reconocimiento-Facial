"""Utilidades de coincidencia de embeddings faciales.

El cálculo del embedding (InsightFace/ArcFace) se realiza en el cliente.
El servidor solo almacena y compara vectores mediante similitud coseno,
lo que mantiene la base de datos portable (PostgreSQL/MySQL) sin depender
de extensiones vectoriales.
"""

import numpy as np

DIM = 512  # dimensión del embedding ArcFace (buffalo_l)


def to_bytes(embedding: list[float]) -> bytes:
    arr = np.asarray(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm
    return arr.tobytes()


def from_bytes(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)


def normalizar(embedding: list[float]) -> np.ndarray:
    arr = np.asarray(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)
    return arr / norm if norm > 0 else arr


def mejor_coincidencia(
    consulta: np.ndarray, candidatos: list[tuple[int, bytes]]
) -> tuple[int | None, float]:
    """Devuelve (empleado_id, score) de la mejor coincidencia por coseno.

    Los vectores almacenados ya están normalizados, por lo que el producto
    punto equivale a la similitud coseno.
    """
    mejor_id: int | None = None
    mejor_score = -1.0
    for emp_id, blob in candidatos:
        if not blob:
            continue
        vec = from_bytes(blob)
        if vec.shape != consulta.shape:
            continue
        score = float(np.dot(consulta, vec))
        if score > mejor_score:
            mejor_score = score
            mejor_id = emp_id
    return mejor_id, mejor_score
