from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_admin
from ..models import Dispositivo

router = APIRouter(prefix="/api/dispositivos", tags=["dispositivos"])


class DispositivoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    ubicacion: str | None = None
    last_seen: datetime | None = None
    online: bool = False


@router.get("", response_model=list[DispositivoOut])
async def listar(db: AsyncSession = Depends(get_db), _=Depends(get_current_admin)):
    dispositivos = (await db.execute(select(Dispositivo))).scalars().all()
    limite = datetime.now(timezone.utc) - timedelta(minutes=5)
    salida = []
    for d in dispositivos:
        out = DispositivoOut.model_validate(d)
        out.online = bool(d.last_seen and d.last_seen >= limite)
        salida.append(out)
    return salida
