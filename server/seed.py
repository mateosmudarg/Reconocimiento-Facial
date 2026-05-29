"""Inicializa la base de datos y crea el primer administrador.

Uso:
    python -m seed            (desde el directorio server/)
"""

import asyncio

from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal, init_models
from app.models import Admin
from app.security import hash_password


async def main() -> None:
    await init_models()
    async with SessionLocal() as db:
        existe = (
            await db.execute(
                select(Admin).where(Admin.username == settings.admin_username)
            )
        ).scalar_one_or_none()
        if existe:
            print(f"El administrador '{settings.admin_username}' ya existe.")
            return
        admin = Admin(
            username=settings.admin_username,
            hashed_password=hash_password(settings.admin_password),
            full_name="Administrador",
            role="admin",
        )
        db.add(admin)
        await db.commit()
        print(f"Administrador '{settings.admin_username}' creado correctamente.")


if __name__ == "__main__":
    asyncio.run(main())
