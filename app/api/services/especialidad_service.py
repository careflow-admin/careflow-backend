from fastapi import HTTPException, status

from app.api.models.especialidad import Especialidad
from app.api.repositories.especialidad_repository import EspecialidadRepository
from app.api.schemas.especialidad import EspecialidadCreate, EspecialidadUpdate
from app.api.services.base import remove_none, schema_to_dict


class EspecialidadService:
    def __init__(self, repo: EspecialidadRepository):
        self.repo = repo

    def list(self) -> list[Especialidad]:
        return self.repo.list()

    def get(self, id_especialidad: int) -> Especialidad:
        especialidad = self.repo.get_by_id(id_especialidad)
        if not especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Especialidad no encontrada.",
            )
        return especialidad

    def create(self, especialidad_in: EspecialidadCreate) -> Especialidad:
        existente = self.repo.get_by_nombre(especialidad_in.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Especialidad ya registrada.",
            )

        especialidad = Especialidad(nombre=especialidad_in.nombre)
        return self.repo.create(especialidad)

    def update(
        self, id_especialidad: int, especialidad_in: EspecialidadUpdate
    ) -> Especialidad:
        especialidad = self.get(id_especialidad)
        data = remove_none(schema_to_dict(especialidad_in))
        if not data:
            return especialidad

        if "nombre" in data and data["nombre"] != especialidad.nombre:
            existente = self.repo.get_by_nombre(data["nombre"])
            if existente and existente.id_especialidad != especialidad.id_especialidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Especialidad ya registrada.",
                )

        return self.repo.update(especialidad, data)

    def delete(self, id_especialidad: int) -> None:
        especialidad = self.get(id_especialidad)
        self.repo.delete(especialidad)
