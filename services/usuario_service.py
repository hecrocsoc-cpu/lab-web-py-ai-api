from datetime import datetime, timezone
from models.usuario import UsuarioCrear, UsuarioDB
from auth.jwt import hashear_password, verificar_password


class UsuarioService:
    def __init__(self):
        self._store = {}  # guardamos usuarios en memoria, clave = email
        self._next_id = 1
        self._crear_admin()

    def _crear_admin(self):
        """Usuario de prueba precargado"""
        admin = UsuarioDB(
            id=self._next_id,
            email="admin@demo.com",
            nombre="Admin",
            rol="admin",
            fecha_registro=datetime.now(timezone.utc),
            password_hash=hashear_password("admin1234"),
        )
        self._store[admin.email] = admin
        self._next_id += 1

    def registrar(self, datos: UsuarioCrear) -> UsuarioDB:
        if datos.email in self._store:
            raise ValueError("El email ya está registrado")

        usuario = UsuarioDB(
            id=self._next_id,
            email=datos.email,
            nombre=datos.nombre,
            rol="usuario",
            fecha_registro=datetime.now(timezone.utc),
            password_hash=hashear_password(datos.password),
        )
        self._store[datos.email] = usuario
        self._next_id += 1
        return usuario

    def autenticar(self, email: str, password: str) -> UsuarioDB:
        usuario = self._store.get(email)
        if not usuario or not verificar_password(password, usuario.password_hash):
            raise ValueError("Email o password incorrectos")
        return usuario

    def obtener_por_email(self, email: str) -> UsuarioDB:
        if email not in self._store:
            raise KeyError(email)
        return self._store[email]


usuario_service = UsuarioService()