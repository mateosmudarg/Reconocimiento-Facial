from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Admin(Base):
    """Usuario del panel administrativo / operador de kiosko."""

    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(120), default="")
    role: Mapped[str] = mapped_column(String(20), default="admin")  # admin | operator
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Empleado(Base):
    __tablename__ = "empleados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), index=True)
    documento: Mapped[str | None] = mapped_column(String(40), unique=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    departamento: Mapped[str | None] = mapped_column(String(80), nullable=True)
    activo: Mapped[bool] = mapped_column(default=True)

    # Embedding facial (vector float32 serializado) y miniatura de referencia.
    embedding: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    foto: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    movimientos: Mapped[list["Movimiento"]] = relationship(
        back_populates="empleado", cascade="all, delete-orphan"
    )


class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    ubicacion: Mapped[str | None] = mapped_column(String(120), nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Movimiento(Base):
    __tablename__ = "movimientos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empleado_id: Mapped[int] = mapped_column(
        ForeignKey("empleados.id", ondelete="CASCADE"), index=True
    )
    tipo: Mapped[str] = mapped_column(String(10), index=True)  # entrada | salida
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    confianza: Mapped[float] = mapped_column(Float, default=0.0)
    dispositivo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    imagen: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)

    empleado: Mapped["Empleado"] = relationship(back_populates="movimientos")
