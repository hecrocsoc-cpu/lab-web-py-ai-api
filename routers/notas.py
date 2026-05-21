from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from auth.jwt import obtener_usuario_actual
from models.nota import NotaCrear, NotaDB
from models.usuario import UsuarioDB
from services.nota_service import nota_service

router = APIRouter(prefix="/notas", tags=["Notas"])

UsuarioActual = Annotated[UsuarioDB, Depends(obtener_usuario_actual)]


@router.get("/")
def listar_notas(
    usuario: UsuarioActual,
    buscar: Optional[str] = Query(None)
) -> List[NotaDB]:
    return nota_service.listar(usuario.id, buscar)


@router.get("/{nota_id}")
def obtener_nota(nota_id: int, usuario: UsuarioActual) -> NotaDB:
    try:
        return nota_service.obtener(nota_id, usuario.id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Nota no encontrada")


@router.post("/", status_code=201)
def crear_nota(datos: NotaCrear, usuario: UsuarioActual) -> NotaDB:
    return nota_service.crear(datos, usuario.id)


@router.put("/{nota_id}")
def editar_nota(nota_id: int, datos: NotaCrear, usuario: UsuarioActual) -> NotaDB:
    try:
        return nota_service.editar(nota_id, datos, usuario.id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Nota no encontrada")


@router.delete("/{nota_id}", status_code=204)
def eliminar_nota(nota_id: int, usuario: UsuarioActual) -> None:
    try:
        nota_service.eliminar(nota_id, usuario.id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Nota no encontrada")