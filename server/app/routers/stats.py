from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_admin
from ..models import Dispositivo, Empleado, Movimiento
from ..presence import ids_dentro
from ..schemas import ActividadItem, PuntoSerie, ResumenStats

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/resumen", response_model=ResumenStats)
async def resumen(db: AsyncSession = Depends(get_db), _=Depends(get_current_admin)):
    total = (await db.execute(select(func.count(Empleado.id)))).scalar_one()
    dentro = await ids_dentro(db)

    inicio_dia = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    entradas = (
        await db.execute(
            select(func.count(Movimiento.id)).where(
                Movimiento.tipo == "entrada", Movimiento.timestamp >= inicio_dia
            )
        )
    ).scalar_one()
    salidas = (
        await db.execute(
            select(func.count(Movimiento.id)).where(
                Movimiento.tipo == "salida", Movimiento.timestamp >= inicio_dia
            )
        )
    ).scalar_one()

    hace_5m = datetime.now(timezone.utc) - timedelta(minutes=5)
    online = (
        await db.execute(
            select(func.count(Dispositivo.id)).where(Dispositivo.last_seen >= hace_5m)
        )
    ).scalar_one()

    return ResumenStats(
        total_empleados=total,
        dentro=len(dentro),
        entradas_hoy=entradas,
        salidas_hoy=salidas,
        dispositivos_online=online,
    )


@router.get("/series", response_model=list[PuntoSerie])
async def series(
    dias: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    inicio = (
        datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        - timedelta(days=dias - 1)
    )
    dia = func.date(Movimiento.timestamp)
    rows = (
        await db.execute(
            select(dia, Movimiento.tipo, func.count(Movimiento.id))
            .where(Movimiento.timestamp >= inicio)
            .group_by(dia, Movimiento.tipo)
        )
    ).all()

    mapa: dict[str, dict[str, int]] = {}
    for fecha_dia, tipo, cant in rows:
        clave = str(fecha_dia)
        mapa.setdefault(clave, {"entrada": 0, "salida": 0})[tipo] = cant

    serie = []
    for i in range(dias):
        f = (inicio + timedelta(days=i)).date().isoformat()
        d = mapa.get(f, {"entrada": 0, "salida": 0})
        serie.append(PuntoSerie(fecha=f, entradas=d["entrada"], salidas=d["salida"]))
    return serie


@router.get("/actividad", response_model=list[ActividadItem])
async def actividad(
    limit: int = Query(15, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    rows = (
        await db.execute(
            select(Movimiento, Empleado.nombre)
            .join(Empleado, Empleado.id == Movimiento.empleado_id)
            .order_by(Movimiento.timestamp.desc())
            .limit(limit)
        )
    ).all()
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
