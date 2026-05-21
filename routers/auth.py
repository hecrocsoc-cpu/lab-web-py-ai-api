from fastapi import APIRouter, HTTPException, status
from models.usuario import UsuarioCrear, UsuarioLogin, TokenRespuesta, UsuarioPublico
from auth.jwt import crear_token
from services.usuario_service import usuario_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro", status_code=201)
def registro(datos: UsuarioCrear) -> TokenRespuesta:
    try:
        usuario = usuario_service.registrar(datos)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    token = crear_token({"sub": usuario.email, "rol": usuario.rol})
    return TokenRespuesta(
        access_token=token,
        usuario=UsuarioPublico(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            rol=usuario.rol,
            fecha_registro=usuario.fecha_registro,
        )
    )


@router.post("/login")
def login(credenciales: UsuarioLogin) -> TokenRespuesta:
    try:
        usuario = usuario_service.autenticar(credenciales.email, credenciales.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Email o password incorrectos")

    token = crear_token({"sub": usuario.email, "rol": usuario.rol})
    return TokenRespuesta(
        access_token=token,
        usuario=UsuarioPublico(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            rol=usuario.rol,
            fecha_registro=usuario.fecha_registro,
        )
    )