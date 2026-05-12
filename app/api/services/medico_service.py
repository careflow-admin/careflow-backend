from fastapi import HTTPException, status

from app.api.models.medico import Medico
from app.api.models.usuario import RolUsuario, Usuario
from app.api.repositories.especialidad_repository import EspecialidadRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.medico import MedicoCreate, MedicoUpdate
from app.api.services.base import remove_none, schema_to_dict


class MedicoService:
    def __init__(
        self,
        medico_repo: MedicoRepository,
        usuario_repo: UsuarioRepository,
        especialidad_repo: EspecialidadRepository,
    ):
        self.medicos = medico_repo
        self.usuarios = usuario_repo
        self.especialidades = especialidad_repo

    def list(self) -> list[Medico]:
        medicos = self.medicos.list()
        return [ {**medico.to_dict(), "especialidad": medico.especialidad.nombre, "data": medico.usuario.to_dict()} for medico in medicos ]

    def get(self, id_medico: int) -> any:
        medico = self.medicos.get_by_id(id_medico)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medico no encontrado.",
            )
        return {**medico.to_dict(), "especialidad": medico.especialidad.nombre, "data": medico.usuario.to_dict()}

    def _validar_usuario_medico(self, id_usuario: int) -> None:
        usuario = self.usuarios.get_by_id(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado.",
            )
        if usuario.rol != RolUsuario.medico:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene rol medico.",
            )

    def _validar_especialidad(self, especialidad_id: int) -> None:
        especialidad = self.especialidades.get_by_id(especialidad_id)
        if not especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Especialidad no encontrada.",
            )

    def create(self, medico_in: MedicoCreate) -> Medico:
        self._validar_usuario_medico(medico_in.id_usuario)

        existente = self.medicos.get_by_usuario_id(medico_in.id_usuario)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya es medico.",
            )

        self._validar_especialidad(medico_in.especialidad_id)

        medico = Medico(
            id_usuario=medico_in.id_usuario,
            especialidad_id=medico_in.especialidad_id,
        )
        return self.medicos.create(medico)

    def update(self, id_medico: int, medico_in: MedicoUpdate) -> Medico:
        medico = self.get(id_medico)
        data = remove_none(schema_to_dict(medico_in))
        if not data:
            return medico

        if "id_usuario" in data:
            self._validar_usuario_medico(data["id_usuario"])
            existente = self.medicos.get_by_usuario_id(data["id_usuario"])
            if existente and existente.id_medico != medico.id_medico:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya es medico.",
                )

        if "especialidad_id" in data:
            self._validar_especialidad(data["especialidad_id"])

        return self.medicos.update(medico, data)

    def delete(self, id_medico: int) -> None:
        medico = self.get(id_medico)
        self.medicos.delete(medico)
