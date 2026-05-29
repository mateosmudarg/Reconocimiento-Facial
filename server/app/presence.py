"""Cálculo de presencia: empleados actualmente dentro de la empresa.

Un empleado está "dentro" si su movimiento más reciente es de tipo 'entrada'.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Movimiento


async def ids_dentro(db: AsyncSession) -> set[int]:
    # Subconsulta: timestamp del último movimiento por empleado.
    ultimo = (
        select(
            Movimiento.empleado_id.label("emp"),
            func.max(Movimiento.timestamp).label("ts"),
        )
        .group_by(Movimiento.empleado_id)
        .subquery()
    )

    stmt = (
        select(Movimiento.empleado_id)
        .join(
            ultimo,
            (Movimiento.empleado_id == ultimo.c.emp)
            & (Movimiento.timestamp == ultimo.c.ts),
        )
        .where(Movimiento.tipo == "entrada")
    )
    result = await db.execute(stmt)
    return {row[0] for row in result.all()}
