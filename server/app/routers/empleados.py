import base64

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_admin, require_admin
from ..face_match import to_bytes
from ..models import Empleado
from ..presence import ids_dentro
from ..schemas import EmpleadoCreate, EmpleadoOut, EmpleadoUpdate

router = APIRouter(prefix="/api/empleados", tags=["empleados"])


def _to_out(emp: Empleado, dentro: set[int]) -> EmpleadoOut:
    return EmpleadoOut(
        id=emp.id,
        nombre=emp.nombre,
        documento=emp.documento,
        email=emp.email,
        departamento=emp.departamento,
        activo=emp.activo,
        created_at=emp.created_at,
        tiene_rostro=emp.embedding is not None,
        dentro=emp.id in dentro,
    )


@router.get("", response_model=list[EmpleadoOut])
async def listar(
    buscar: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    stmt = select(Empleado).order_by(Empleado.nombre)
    if buscar:
        like = f"%{buscar}%"
        stmt = stmt.where(
            or_(
                Empleado.nombre.ilike(like),
                Empleado.documento.ilike(like),
                Empleado.departamento.ilike(like),
            )
        )
    empleados = (await db.execute(stmt)).scalars().all()
    dentro = await ids_dentro(db)
    return [_to_out(e, dentro) for e in empleados]


@router.post("", response_model=EmpleadoOut, status_code=201)
async def crear(
    data: EmpleadoCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    foto = base64.b64decode(data.foto_b64) if data.foto_b64 else None
    emp = Empleado(
        nombre=data.nombre,
        documento=data.documento,
        email=data.email,
        departamento=data.departamento,
        activo=data.activo,
        embedding=to_bytes(data.embedding),
        foto=foto,
    )
    db.add(emp)
    try:
        await db.commit()
    except Exception as e:  # p.ej. documento duplicado
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"No se pudo crear: {e}")
    await db.refresh(emp)
    return _to_out(emp, set())


@router.patch("/{empleado_id}", response_model=EmpleadoOut)
async def actualizar(
    empleado_id: int,
    data: EmpleadoUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    emp = await db.get(Empleado, empleado_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    campos = data.model_dump(exclude_unset=True)
    if "embedding" in campos and campos["embedding"] is not None:
        emp.embedding = to_bytes(campos.pop("embedding"))
    else:
        campos.pop("embedding", None)
    if "foto_b64" in campos:
        foto_b64 = campos.pop("foto_b64")
        emp.foto = base64.b64decode(foto_b64) if foto_b64 else None
    for k, v in campos.items():
        setattr(emp, k, v)

    await db.commit()
    await db.refresh(emp)
    dentro = await ids_dentro(db)
    return _to_out(emp, dentro)


@router.delete("/{empleado_id}", status_code=204)
async def eliminar(
    empleado_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin),
):
    emp = await db.get(Empleado, empleado_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    await db.delete(emp)
    await db.commit()
