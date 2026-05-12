from fastapi import HTTPException, status

from app.api.models.usuario import Usuario
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.api.services.base import remove_none, schema_to_dict
from app.security.passwords import hash_password

class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def list(self) -> list[Usuario]:
        return self.repo.list()

    def get(self, id_usuario: int) -> Usuario:
        usuario = self.repo.get_by_id(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado.",
            )
        return usuario

    def create(self, usuario_in: UsuarioCreate) -> Usuario:
        existente = self.repo.get_by_correo(usuario_in.correo)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Correo ya registrado.",
            )

        usuario = Usuario(
            nombre=usuario_in.nombre,
            correo=usuario_in.correo,
            contrasena_hash=hash_password(usuario_in.contrasena),
            rol=usuario_in.rol,
        )
        return self.repo.create(usuario)

    def update(self, id_usuario: int, usuario_in: UsuarioUpdate) -> Usuario:
        usuario = self.get(id_usuario)
        data = remove_none(schema_to_dict(usuario_in))
        if not data:
            return usuario

        if "correo" in data and data["correo"] != usuario.correo:
            existente = self.repo.get_by_correo(data["correo"])
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Correo ya registrado.",
                )

        if "contrasena" in data:
            data["contrasena_hash"] = hash_password(data.pop("contrasena"))

        return self.repo.update(usuario, data)

    def delete(self, id_usuario: int) -> None:
        usuario = self.get(id_usuario)
        self.repo.delete(usuario)
