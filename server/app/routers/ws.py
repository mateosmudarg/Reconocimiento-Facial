from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..realtime import manager
from ..security import decode_token

router = APIRouter()


@router.websocket("/ws/monitor")
async def monitor(ws: WebSocket, token: str = ""):
    """Canal de monitoreo en tiempo real. Requiere ?token=<jwt>."""
    payload = decode_token(token)
    if not payload:
        await ws.close(code=4401)
        return

    await manager.connect(ws)
    try:
        while True:
            # Mantiene viva la conexión; ignora mensajes entrantes.
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(ws)
    except Exception:
        await manager.disconnect(ws)
