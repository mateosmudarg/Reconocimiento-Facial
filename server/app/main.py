from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import init_models
from .routers import (
    auth,
    dispositivos,
    empleados,
    movimientos,
    reconocimiento,
    stats,
    ws,
)

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(
    title="RecFac · API de Control de Accesos",
    version="2.0.0",
    description="Sistema centralizado de control de ingresos/egresos por reconocimiento facial.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(empleados.router)
app.include_router(reconocimiento.router)
app.include_router(movimientos.router)
app.include_router(stats.router)
app.include_router(dispositivos.router)
app.include_router(ws.router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse(STATIC_DIR / "dashboard.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
