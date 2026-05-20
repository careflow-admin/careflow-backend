import logging
from typing import Optional

from fastapi import HTTPException, status

from app.api.models.receta_medica import RecetaMedica
from app.api.repositories.historial_clinico_repository import HistorialClinicoRepository
from app.api.repositories.medicamento_repository import MedicamentoRepository
from app.api.repositories.receta_medica_repository import RecetaMedicaRepository
from app.api.schemas.receta_medica import RecetaMedicaCreate, RecetaMedicaUpdate
from app.api.services.base import remove_none, schema_to_dict
from app.utils.email import send_receta_medica_email

logger = logging.getLogger(__name__)


class RecetaMedicaService:
    def __init__(
        self,
        receta_repo: RecetaMedicaRepository,
        historial_repo: HistorialClinicoRepository,
        medicamento_repo: MedicamentoRepository,
    ):
        self.recetas = receta_repo
        self.historiales = historial_repo
        self.medicamentos = medicamento_repo

    def _get_historial(self, id_historial: int):
        historial = self.historiales.get_by_id(id_historial)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial clinico no encontrado.",
            )
        return historial

    def _get_medicamento(self, id_medicamento: int):
        medicamento = self.medicamentos.get_by_id(id_medicamento)
        if not medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medicamento no encontrado.",
            )
        return medicamento

    def list(self, id_historial: Optional[int] = None) -> list[RecetaMedica]:
        if id_historial is not None:
            self._get_historial(id_historial)
            return self.recetas.list_by_historial(id_historial)
        return self.recetas.list()

    def get(self, id_receta: int) -> RecetaMedica:
        receta = self.recetas.get_by_id(id_receta)
        if not receta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receta medica no encontrada.",
            )
        return receta

    def create(self, receta_in: RecetaMedicaCreate) -> RecetaMedica:
        historial = self._get_historial(receta_in.id_historial)
        medicamento = self._get_medicamento(receta_in.id_medicamento)

        receta = RecetaMedica(
            id_historial=receta_in.id_historial,
            id_medicamento=receta_in.id_medicamento,
            dosis=receta_in.dosis,
            frecuencia=receta_in.frecuencia,
            duracion=receta_in.duracion,
            indicaciones=receta_in.indicaciones,
        )
        created = self.recetas.create(receta)
        self._notify_receta_email(created, historial, medicamento)
        return created

    def update(self, id_receta: int, receta_in: RecetaMedicaUpdate) -> RecetaMedica:
        receta = self.get(id_receta)
        data = remove_none(schema_to_dict(receta_in))
        if not data:
            return receta

        if "id_historial" in data:
            self._get_historial(data["id_historial"])
        if "id_medicamento" in data:
            self._get_medicamento(data["id_medicamento"])

        return self.recetas.update(receta, data)

    def delete(self, id_receta: int) -> None:
        receta = self.get(id_receta)
        self.recetas.delete(receta)

    def _notify_receta_email(self, receta: RecetaMedica, historial, medicamento) -> None:
        paciente = getattr(historial, "paciente", None)
        if not paciente or not paciente.correo:
            return

        medico = getattr(historial, "medico", None)
        medico_nombre = "Medico"
        especialidad = ""
        if medico and medico.usuario:
            medico_nombre = medico.usuario.nombre
        if medico and medico.especialidad:
            especialidad = medico.especialidad.nombre

        try:
            send_receta_medica_email(
                to_email=paciente.correo,
                paciente_nombre=paciente.nombre,
                medico_nombre=medico_nombre,
                especialidad=especialidad,
                medicamento_nombre=medicamento.nombre,
                medicamento_descripcion=medicamento.descripcion,
                dosis=receta.dosis,
                frecuencia=receta.frecuencia,
                duracion=receta.duracion,
                indicaciones=receta.indicaciones,
                dosis_recomendada=medicamento.dosis_recomendada,
                contraindicaciones=medicamento.contraindicaciones,
            )
        except Exception:
            logger.exception(
                "Error sending receta email for receta %s", receta.id_receta
            )
