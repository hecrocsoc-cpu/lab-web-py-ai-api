from datetime import datetime, timezone
from typing import List, Optional
from models.nota import NotaCrear, NotaDB


class NotaService:
    def __init__(self):
        self._store = {}  # clave = id de la nota
        self._next_id = 1

    def crear(self, datos: NotaCrear, usuario_id: int) -> NotaDB:
        ahora = datetime.now(timezone.utc)
        nota = NotaDB(
            id=self._next_id,
            titulo=datos.titulo,
            contenido=datos.contenido,
            etiquetas=datos.etiquetas,
            usuario_id=usuario_id,
            fecha_creacion=ahora,
            fecha_actualizacion=ahora,
        )
        self._store[self._next_id] = nota
        self._next_id += 1
        return nota

    def listar(self, usuario_id: int, buscar: Optional[str] = None) -> List[NotaDB]:
        notas = [n for n in self._store.values() if n.usuario_id == usuario_id]
        if buscar:
            q = buscar.lower()
            notas = [n for n in notas if q in n.titulo.lower() or q in n.contenido.lower()]
        return notas

    def obtener(self, nota_id: int, usuario_id: int) -> NotaDB:
        nota = self._store.get(nota_id)
        if not nota or nota.usuario_id != usuario_id:
            raise KeyError(nota_id)
        return nota

    def editar(self, nota_id: int, datos: NotaCrear, usuario_id: int) -> NotaDB:
        existente = self.obtener(nota_id, usuario_id)
        actualizada = NotaDB(
            id=nota_id,
            titulo=datos.titulo,
            contenido=datos.contenido,
            etiquetas=datos.etiquetas,
            usuario_id=usuario_id,
            fecha_creacion=existente.fecha_creacion,
            fecha_actualizacion=datetime.now(timezone.utc),
        )
        self._store[nota_id] = actualizada
        return actualizada

    def eliminar(self, nota_id: int, usuario_id: int) -> None:
        self.obtener(nota_id, usuario_id)
        del self._store[nota_id]

    def total_por_usuario(self, usuario_id: int) -> int:
        return sum(1 for n in self._store.values() if n.usuario_id == usuario_id)


nota_service = NotaService()