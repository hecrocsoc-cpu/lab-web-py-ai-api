from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class UsuarioCrear(BaseModel):
    """Lo que el cliente envía al registrarse"""
    email: str
    password: str = Field(..., min_length=8)
    nombre: str

class UsuarioLogin(BaseModel):
    """Lo que el cliente envía al hacer login"""
    email: str
    password: str

class UsuarioDB(BaseModel):
    """Lo que guardamos internamente (con el hash del password)"""
    id: int
    email: str
    nombre: str
    rol: str = "usuario"
    fecha_registro: datetime
    password_hash: str

class UsuarioPublico(BaseModel):
    """Lo que devolvemos al cliente (SIN el password)"""
    id: int
    email: str
    nombre: str
    rol: str
    fecha_registro: datetime

class TokenRespuesta(BaseModel):
    """Respuesta del login/registro"""
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioPublico