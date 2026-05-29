from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..deps import get_current_admin
from ..models import Admin
from ..schemas import AdminOut, Token
from ..security import create_access_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Admin).where(Admin.username == form.username))
    admin = result.scalar_one_or_none()
    if not admin or not verify_password(form.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    if not admin.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    token = create_access_token(admin.username, admin.role)
    return Token(
        access_token=token, role=admin.role, full_name=admin.full_name or admin.username
    )


@router.get("/me", response_model=AdminOut)
async def me(admin: Admin = Depends(get_current_admin)):
    return admin
