from typing import Optional

from fastapi import HTTPException, status

from app.api.models.historial_clinico import HistorialClinico
from app.api.models.usuario import RolUsuario
from app.api.repositories.historial_clinico_repository import HistorialClinicoRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.historial_clinico import (
    HistorialClinicoCreate,
    HistorialClinicoUpdate,
)
from app.api.services.base import remove_none, schema_to_dict


class HistorialClinicoService:
    def __init__(
        self,
        historial_repo: HistorialClinicoRepository,
        usuario_repo: UsuarioRepository,
        medico_repo: MedicoRepository,
    ):
        self.historiales = historial_repo
        self.usuarios = usuario_repo
        self.medicos = medico_repo

    def _get_historial(self, id_historial: int) -> HistorialClinico:
        historial = self.historiales.get_by_id(id_historial)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial clinico no encontrado.",
            )
        return historial

    def _validar_paciente(self, id_paciente: int) -> None:
        paciente = self.usuarios.get_by_id(id_paciente)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado.",
            )
        if paciente.rol != RolUsuario.paciente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene rol paciente.",
            )

    def _validar_medico(self, id_medico: int) -> None:
        medico = self.medicos.get_by_id(id_medico)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medico no encontrado.",
            )

    def list(
        self,
        paciente_id: Optional[int] = None,
        medico_id: Optional[int] = None,
    ) -> list[HistorialClinico]:
        return self.historiales.list(paciente_id=paciente_id, medico_id=medico_id)

    def get(self, id_historial: int) -> HistorialClinico:
        return self._get_historial(id_historial)

    def create(self, historial_in: HistorialClinicoCreate) -> HistorialClinico:
        self._validar_paciente(historial_in.id_paciente)
        self._validar_medico(historial_in.id_medico)

        historial = HistorialClinico(
            id_paciente=historial_in.id_paciente,
            id_medico=historial_in.id_medico,
            motivo=historial_in.motivo,
            diagnostico=historial_in.diagnostico,
            sintomas=historial_in.sintomas,
            observaciones=historial_in.observaciones,
            tratamiento=historial_in.tratamiento,
        )
        return self.historiales.create(historial)

    def update(
        self, id_historial: int, historial_in: HistorialClinicoUpdate
    ) -> HistorialClinico:
        historial = self._get_historial(id_historial)
        data = remove_none(schema_to_dict(historial_in))
        if not data:
            return historial

        if "id_paciente" in data:
            self._validar_paciente(data["id_paciente"])
        if "id_medico" in data:
            self._validar_medico(data["id_medico"])

        return self.historiales.update(historial, data)

    def delete(self, id_historial: int) -> None:
        historial = self._get_historial(id_historial)
        self.historiales.delete(historial)
