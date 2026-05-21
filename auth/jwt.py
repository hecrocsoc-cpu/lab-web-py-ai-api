from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings

# Herramienta para hashear passwords con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Le dice a FastAPI que el token viene en el header: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hashear_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verificar_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def crear_token(datos: dict) -> str:
    payload = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expira
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def obtener_usuario_actual(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    from services.usuario_service import usuario_service  # import local para evitar ciclo

    payload = decodificar_token(token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Token sin usuario")

    return usuario_service.obtener_por_email(email)