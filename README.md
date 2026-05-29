# 🎯 RecFac · Control de Accesos por Reconocimiento Facial

Sistema **cliente-servidor** para el control de ingresos y egresos de personal
de una empresa mediante reconocimiento facial. Reemplaza por completo la versión
monolítica anterior (Tkinter + SQLite + Haar Cascade) por una arquitectura
moderna, escalable y lista para producción.

---

## 🏗️ Arquitectura

```
┌──────────────────────────┐         REST + WebSocket        ┌───────────────────────────┐
│  CLIENTE (Kiosko/Cámara)  │  ───────────────────────────▶  │  SERVIDOR (API central)    │
│  PySide6 + InsightFace    │                                 │  FastAPI + PostgreSQL      │
│  · Captura de cámara      │   embeddings (512-d, ArcFace)   │  · Auth JWT                │
│  · Detección + embedding  │  ◀───────────────────────────  │  · Empleados / Movimientos │
│  · Registro entrada/salida│         resultado + evento      │  · Estadísticas            │
│  · Sincronización         │                                 │  · Monitoreo en vivo (WS)  │
│  · Control puerta Arduino │                                 │  · Dashboard web           │
└──────────────────────────┘                                 └───────────────────────────┘
```

- **El reconocimiento corre en el cliente** (InsightFace/ArcFace), distribuyendo
  la carga de cómputo. El servidor solo almacena y compara *embeddings* por
  similitud coseno → base de datos portable, sin extensiones vectoriales.
- **Tiempo real** vía WebSocket: cada movimiento se transmite al panel al instante.

```
server/        API FastAPI + dashboard web administrativo
  app/
    routers/   auth · empleados · reconocimiento · movimientos · stats · dispositivos · ws
    static/    dashboard.html (panel de control con gráficos)
  seed.py      crea las tablas y el primer administrador
client/        Aplicación de escritorio (PySide6)
  app/
    ui/        login · ventana principal · alta de empleados
    face_engine.py · camera.py · worker.py · api_client.py · arduino_serial.py
arduino/        Sketch para apertura de puerta vía serie
```

---

## 🚀 Puesta en marcha

### 1. Base de datos (PostgreSQL)

```sql
CREATE DATABASE recfac;
CREATE USER recfac WITH PASSWORD 'recfac';
GRANT ALL PRIVILEGES ON DATABASE recfac TO recfac;
```
> También se soporta MySQL: usar `mysql+aiomysql://...` en `DATABASE_URL`.

### 2. Servidor

```bash
cd server
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
copy .env.example .env                              # editar credenciales
python -m seed                                      # crea tablas + admin
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Panel administrativo: **http://localhost:8000/**
- Documentación interactiva de la API: **http://localhost:8000/docs**

### 3. Cliente

```bash
cd client
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env                              # editar SERVER_URL / cámara
python -m app.main
```

> La primera ejecución del cliente descarga el modelo InsightFace (`buffalo_l`).

---

## ✨ Funcionalidades

**Cliente (kiosko)**
- Cámara en vivo con detección de rostros superpuesta y multi-persona.
- Registro de **entrada / salida** con un clic; valida estado (evita doble registro).
- Alta de empleados capturando el rostro (solo rol *admin*).
- Apertura de puerta opcional vía Arduino.

**Servidor / Panel administrativo**
- Autenticación segura (JWT + bcrypt) con roles `admin` / `operator`.
- Dashboard con: personas **dentro** en tiempo real, entradas/salidas del día,
  gráfico de 30 días, actividad reciente en vivo y estado de cámaras.
- Administración de empleados (CRUD + búsqueda).
- Registros históricos con filtros (tipo, fecha, empleado) y búsqueda.
- API REST documentada (OpenAPI) + WebSocket de monitoreo.

---

## 🔬 Reconocimiento facial

| Antes                              | Ahora                                            |
|------------------------------------|--------------------------------------------------|
| Haar Cascade + `cv2.absdiff`       | InsightFace (detección SCRFD + ArcFace)          |
| Diferencia de píxeles en escala gris | Embeddings 512-d + similitud coseno            |
| Sensible a luz/ángulo, 1 rostro    | Robusto a iluminación/ángulos, multi-rostro      |
| Comparación O(n) con imágenes      | Comparación vectorial rápida y estable           |

El umbral de coincidencia es configurable (`FACE_MATCH_THRESHOLD`).

---

## 🔐 Seguridad y producción

- Cambiar `SECRET_KEY` y las credenciales del admin antes de desplegar.
- Servir tras HTTPS (la conexión WebSocket usará `wss://` automáticamente).
- Restringir `CORS` en `server/app/main.py` a los orígenes necesarios.
- Para esquemas versionados usar Alembic (las tablas se autocrean en arranque
  para facilitar el desarrollo).
