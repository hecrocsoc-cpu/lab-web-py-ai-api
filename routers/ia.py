import uuid
from datetime import datetime, timezone
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from auth.jwt import obtener_usuario_actual
from models.nota import MensajeChat
from models.usuario import UsuarioDB
from services.nota_service import nota_service

router = APIRouter(prefix="/api", tags=["IA"])

UsuarioActual = Annotated[UsuarioDB, Depends(obtener_usuario_actual)]

# Guardamos el historial de chat en memoria
historial_db = {}


@router.post("/chat")
def chat(mensaje: MensajeChat, usuario: UsuarioActual):
    # Crear sesión nueva si no viene session_id
    sid = mensaje.session_id or str(uuid.uuid4())

    if sid not in historial_db:
        historial_db[sid] = []

    # Guardar mensaje del usuario
    historial_db[sid].append({
        "rol": "usuario",
        "contenido": mensaje.contenido,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    # Generar respuesta (simulada — aquí conectarías un LLM real)
    notas = nota_service.listar(usuario.id)
    num_notas = len(notas)
    respuesta = (
        f"Hola {usuario.nombre}, tienes {num_notas} nota(s). "
        f"Me preguntaste: '{mensaje.contenido}'. "
        "Puedo ayudarte a buscar o resumir tus notas."
    )

    # Guardar respuesta del asistente
    historial_db[sid].append({
        "rol": "asistente",
        "contenido": respuesta,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    return {
        "session_id": sid,
        "respuesta": respuesta,
        "num_mensajes_historial": len(historial_db[sid]),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/chat/history/{session_id}")
def obtener_historial(session_id: str, usuario: UsuarioActual):
    if session_id not in historial_db:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    return {
        "ok": True,
        "data": {
            "session_id": session_id,
            "total_mensajes": len(historial_db[session_id]),
            "mensajes": historial_db[session_id]
        }
    }


@router.delete("/chat/history/{session_id}", status_code=204)
def limpiar_historial(session_id: str, usuario: UsuarioActual):
    historial_db.pop(session_id, None)


@router.get("/search")
def buscar(
    usuario: UsuarioActual,
    q: str = Query(..., min_length=1)
):
    notas = nota_service.listar(usuario.id, buscar=q)
    return [
        {
            "id": n.id,
            "titulo": n.titulo,
            "fragmento": n.contenido[:150],
            "etiquetas": n.etiquetas
        }
        for n in notas
    ]


@router.get("/context")
def contexto():
    return {
        "nombre": "Notas IA API",
        "version": "1.0.0",
        "descripcion": "API de notas con autenticación JWT y endpoints para agentes de IA",
        "endpoints": [
            {"metodo": "POST", "ruta": "/auth/registro", "descripcion": "Registrar usuario"},
            {"metodo": "POST", "ruta": "/auth/login", "descripcion": "Login → JWT"},
            {"metodo": "GET",  "ruta": "/notas", "descripcion": "Listar notas"},
            {"metodo": "POST", "ruta": "/notas", "descripcion": "Crear nota"},
            {"metodo": "PUT",  "ruta": "/notas/{id}", "descripcion": "Editar nota"},
            {"metodo": "DELETE", "ruta": "/notas/{id}", "descripcion": "Eliminar nota"},
            {"metodo": "POST", "ruta": "/api/chat", "descripcion": "Chat con historial"},
            {"metodo": "GET",  "ruta": "/api/chat/history/{id}", "descripcion": "Historial"},
            {"metodo": "GET",  "ruta": "/api/search", "descripcion": "Buscar en notas"},
            {"metodo": "GET",  "ruta": "/api/context", "descripcion": "Este endpoint"},
        ]
    }