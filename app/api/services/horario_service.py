from typing import List

from fastapi import HTTPException, status

from app.api.models.horario import Horario
from app.api.repositories.horario_repository import HorarioRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.schemas.horario import HorarioCreate, HorarioUpdate
from app.api.services.base import remove_none, schema_to_dict


class HorarioService:
    def __init__(self, horario_repo: HorarioRepository, medico_repo: MedicoRepository):
        self.horarios = horario_repo
        self.medicos = medico_repo

    def list(self) -> List[Horario]:
        return self.horarios.list()

    def get_disponibilidad(self, id_medico: int) -> List[Horario]:
        self._validar_medico(id_medico)
        return self.horarios.list_by_medico(id_medico)

    def get(self, id_horario: int) -> Horario:
        horario = self.horarios.get_by_id(id_horario)
        if not horario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Horario no encontrado.",
            )
        return horario

    def _validar_medico(self, id_medico: int) -> None:
        medico = self.medicos.get_by_id(id_medico)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medico no encontrado.",
            )

    def create(self, horario_in: HorarioCreate) -> Horario:
        self._validar_medico(horario_in.id_medico)

        horario = Horario(
            id_medico=horario_in.id_medico,
            dia=horario_in.dia,
            hora_inicio=horario_in.hora_inicio,
            hora_fin=horario_in.hora_fin,
        )
        return self.horarios.create(horario)

    def update(self, id_horario: int, horario_in: HorarioUpdate) -> Horario:
        horario = self.get(id_horario)
        data = remove_none(schema_to_dict(horario_in))
        if not data:
            return horario

        if "id_medico" in data:
            self._validar_medico(data["id_medico"])

        return self.horarios.update(horario, data)

    def delete(self, id_horario: int) -> None:
        horario = self.get(id_horario)
        self.horarios.delete(horario)
