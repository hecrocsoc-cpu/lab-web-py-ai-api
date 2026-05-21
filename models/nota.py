from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class NotaCrear(BaseModel):
    """Lo que el cliente envía para crear una nota"""
    titulo: str = Field(..., min_length=3)
    contenido: str
    etiquetas: List[str] = []

class NotaDB(BaseModel):
    """Lo que guardamos internamente"""
    id: int
    titulo: str
    contenido: str
    etiquetas: List[str]
    usuario_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

class MensajeChat(BaseModel):
    """Entrada para el chat con IA"""
    contenido: str
    session_id: Optional[str] = None