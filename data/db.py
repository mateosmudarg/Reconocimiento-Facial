from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date
from data.read_config import read_config

engine = None
SessionLocal = None

Base = declarative_base()


def init_engine():
    global engine, SessionLocal

    if engine:
        return

    config = read_config("database")

    if not config:
        raise Exception("Configuración de base de datos no encontrada")

    DATABASE_URL = config.get("url")

    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():
    if not SessionLocal:
        init_engine()
    return SessionLocal()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    nombre = Column(String(100), nullable=False)
    imagen = Column(LargeBinary)

    movimientos = relationship(
        "Movimiento",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    fk_id_usuarios = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )
    fecha = Column(Date, nullable=False)
    imagen = Column(LargeBinary)
    tipo = Column(String(20), nullable=False)

    usuario = relationship("Usuario", back_populates="movimientos")


def agregar_usuario(nombre, imagen):
    session = get_session()
    try:
        usuario = Usuario(
            fecha=date.today(),
            nombre=nombre,
            imagen=bytes(imagen) if imagen else None
        )
        session.add(usuario)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise Exception(f"Error en base de datos: {e}")
    finally:
        session.close()


def obtener_usuarios(asc=True, limit=10):
    session = get_session()
    try:
        query = session.query(Usuario)
        query = query.order_by(Usuario.id.asc() if asc else Usuario.id.desc())

        if limit != 0:
            query = query.limit(limit)

        resultados = query.all()

        return [
            (u.id, u.fecha, u.nombre, u.imagen)
            for u in resultados
        ]

    finally:
        session.close()


def agregar_movimiento(id_usuario, fecha, imagen, tipo):
    session = get_session()
    try:
        movimiento = Movimiento(
            fk_id_usuarios=id_usuario,
            fecha=fecha if isinstance(fecha, date) else date.today(),
            imagen=bytes(imagen) if imagen else None,
            tipo=tipo
        )
        session.add(movimiento)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise Exception(f"Error en base de datos: {e}")
    finally:
        session.close()


def obtener_movimientos(limit=10):
    session = get_session()
    try:
        query = session.query(Movimiento).order_by(Movimiento.id.desc())

        if limit != 0:
            query = query.limit(limit)

        resultados = query.all()

        return [
            (m.id, m.fk_id_usuarios, m.fecha, m.imagen, m.tipo)
            for m in resultados
        ]

    finally:
        session.close()


def eliminar_usuarios_por_ids(ids):
    if not ids:
        return False

    session = get_session()
    try:
        session.query(Usuario).filter(Usuario.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise Exception(f"Error en base de datos: {e}")
    finally:
        session.close()