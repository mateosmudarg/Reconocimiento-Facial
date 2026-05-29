from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


class AdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool


class AdminCreate(BaseModel):
    username: str
    password: str
    full_name: str = ""
    role: str = "operator"


# ---------- Empleados ----------
class EmpleadoBase(BaseModel):
    nombre: str
    documento: str | None = None
    email: str | None = None
    departamento: str | None = None
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    # Embedding facial como lista de floats (enviado por el cliente).
    embedding: list[float]
    # Miniatura JPEG en base64 (opcional).
    foto_b64: str | None = None


class EmpleadoUpdate(BaseModel):
    nombre: str | None = None
    documento: str | None = None
    email: str | None = None
    departamento: str | None = None
    activo: bool | None = None
    embedding: list[float] | None = None
    foto_b64: str | None = None


class EmpleadoOut(EmpleadoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    tiene_rostro: bool = True
    dentro: bool = False


# ---------- Movimientos ----------
class IdentificarRequest(BaseModel):
    embedding: list[float]
    tipo: str  # entrada | salida
    dispositivo: str | None = None
    imagen_b64: str | None = None


class MovimientoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    empleado_id: int
    tipo: str
    timestamp: datetime
    confianza: float
    dispositivo: str | None = None


class IdentificarResponse(BaseModel):
    ok: bool
    empleado_id: int | None = None
    nombre: str | None = None
    tipo: str | None = None
    confianza: float = 0.0
    timestamp: datetime | None = None
    mensaje: str = ""


# ---------- Stats ----------
class ResumenStats(BaseModel):
    total_empleados: int
    dentro: int
    entradas_hoy: int
    salidas_hoy: int
    dispositivos_online: int


class PuntoSerie(BaseModel):
    fecha: str
    entradas: int
    salidas: int


class ActividadItem(BaseModel):
    id: int
    nombre: str
    tipo: str
    timestamp: datetime
    confianza: float
    dispositivo: str | None = None
