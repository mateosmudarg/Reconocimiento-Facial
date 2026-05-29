import base64
from datetime import date, datetime, time, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_admin
from ..models import Empleado, Movimiento
from ..schemas import ActividadItem

router = APIRouter(prefix="/api/movimientos", tags=["movimientos"])


@router.get("", response_model=list[ActividadItem])
async def listar(
    tipo: str | None = Query(None, pattern="^(entrada|salida)$"),
    empleado_id: int | None = None,
    desde: date | None = None,
    hasta: date | None = None,
    buscar: str | None = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    stmt = (
        select(Movimiento, Empleado.nombre)
        .join(Empleado, Empleado.id == Movimiento.empleado_id)
        .order_by(Movimiento.timestamp.desc())
    )
    if tipo:
        stmt = stmt.where(Movimiento.tipo == tipo)
    if empleado_id:
        stmt = stmt.where(Movimiento.empleado_id == empleado_id)
    if desde:
        stmt = stmt.where(
            Movimiento.timestamp >= datetime.combine(desde, time.min, tzinfo=timezone.utc)
        )
    if hasta:
        stmt = stmt.where(
            Movimiento.timestamp <= datetime.combine(hasta, time.max, tzinfo=timezone.utc)
        )
    if buscar:
        stmt = stmt.where(Empleado.nombre.ilike(f"%{buscar}%"))

    stmt = stmt.limit(limit).offset(offset)
    rows = (await db.execute(stmt)).all()
    return [
        ActividadItem(
            id=m.id,
            nombre=nombre,
            tipo=m.tipo,
            timestamp=m.timestamp,
            confianza=m.confianza,
            dispositivo=m.dispositivo,
        )
        for m, nombre in rows
    ]


@router.get("/{movimiento_id}/imagen")
async def imagen(
    movimiento_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    mov = await db.get(Movimiento, movimiento_id)
    if not mov or not mov.imagen:
        raise HTTPException(status_code=404, detail="Sin imagen")
    return Response(content=mov.imagen, media_type="image/jpeg")
