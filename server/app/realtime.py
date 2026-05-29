import asyncio

from fastapi import WebSocket


class ConnectionManager:
    """Gestiona conexiones WebSocket para el monitoreo en tiempo real."""

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(ws)

    async def broadcast(self, message: dict) -> None:
        async with self._lock:
            conns = list(self._connections)
        muertas: list[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception:
                muertas.append(ws)
        if muertas:
            async with self._lock:
                for ws in muertas:
                    self._connections.discard(ws)


manager = ConnectionManager()
