import base64
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db
from ..deps import get_current_admin
from ..face_match import mejor_coincidencia, normalizar
from ..models import Dispositivo, Empleado, Movimiento
from ..presence import ids_dentro
from ..realtime import manager
from ..schemas import IdentificarRequest, IdentificarResponse

router = APIRouter(prefix="/api/reconocimiento", tags=["reconocimiento"])


@router.post("/identificar", response_model=IdentificarResponse)
async def identificar(
    req: IdentificarRequest,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    if req.tipo not in ("entrada", "salida"):
        return IdentificarResponse(ok=False, mensaje="Tipo de movimiento inválido")

    consulta = normalizar(req.embedding)

    # Candidatos: empleados activos con embedding registrado.
    rows = (
        await db.execute(
            select(Empleado.id, Empleado.embedding).where(
                Empleado.activo.is_(True), Empleado.embedding.isnot(None)
            )
        )
    ).all()
    candidatos = [(r[0], r[1]) for r in rows]

    emp_id, score = mejor_coincidencia(consulta, candidatos)
    if emp_id is None or score < settings.face_match_threshold:
        return IdentificarResponse(
            ok=False, confianza=max(score, 0.0), mensaje="Rostro no reconocido"
        )

    empleado = await db.get(Empleado, emp_id)

    # Evitar doble registro del mismo tipo (ya está dentro/fuera).
    dentro = await ids_dentro(db)
    ya_dentro = emp_id in dentro
    if req.tipo == "entrada" and ya_dentro:
        return IdentificarResponse(
            ok=False,
            empleado_id=emp_id,
            nombre=empleado.nombre,
            confianza=score,
            mensaje=f"{empleado.nombre} ya registró entrada",
        )
    if req.tipo == "salida" and not ya_dentro:
        return IdentificarResponse(
            ok=False,
            empleado_id=emp_id,
            nombre=empleado.nombre,
            confianza=score,
            mensaje=f"{empleado.nombre} no tiene una entrada activa",
        )

    imagen = base64.b64decode(req.imagen_b64) if req.imagen_b64 else None
    mov = Movimiento(
        empleado_id=emp_id,
        tipo=req.tipo,
        confianza=round(score, 4),
        dispositivo=req.dispositivo,
        imagen=imagen,
    )
    db.add(mov)

    if req.dispositivo:
        disp = (
            await db.execute(
                select(Dispositivo).where(Dispositivo.nombre == req.dispositivo)
            )
        ).scalar_one_or_none()
        now = datetime.now(timezone.utc)
        if disp:
            disp.last_seen = now
        else:
            db.add(Dispositivo(nombre=req.dispositivo, last_seen=now))

    await db.commit()
    await db.refresh(mov)

    await manager.broadcast(
        {
            "evento": "movimiento",
            "empleado_id": emp_id,
            "nombre": empleado.nombre,
            "tipo": req.tipo,
            "confianza": round(score, 4),
            "dispositivo": req.dispositivo,
            "timestamp": mov.timestamp.isoformat(),
        }
    )

    return IdentificarResponse(
        ok=True,
        empleado_id=emp_id,
        nombre=empleado.nombre,
        tipo=req.tipo,
        confianza=round(score, 4),
        timestamp=mov.timestamp,
        mensaje=f"{'Bienvenido' if req.tipo == 'entrada' else 'Hasta luego'}, {empleado.nombre}",
    )
