import logging
from typing import Any, List, Optional

from fastapi import HTTPException, status

from app.api.models.cita import Cita, EstadoCita
from app.api.models.medico import Medico
from app.api.models.usuario import RolUsuario, Usuario
from app.api.repositories.cita_repository import CitaRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.cita import CitaCreate, CitaUpdate
from app.api.services.base import remove_none, schema_to_dict
from app.utils.email import send_cita_estado_email

logger = logging.getLogger(__name__)


class CitaService:
    def __init__(
        self,
        cita_repo: CitaRepository,
        usuario_repo: UsuarioRepository,
        medico_repo: MedicoRepository,
    ):
        self.citas = cita_repo
        self.usuarios = usuario_repo
        self.medicos = medico_repo

    def _build_medico_data(self, medico: Medico) -> dict[str, Any]:
        return {
            **medico.to_dict(),
            "especialidad": medico.especialidad.nombre,
            "data": {
                "nombre": medico.usuario.nombre,
                "rol": medico.usuario.rol.value,
            },
        }

    def _build_cita_data(self, cita: Cita) -> dict[str, Any]:
        return {**cita.to_dict(), "medico": self._build_medico_data(cita.medico)}

    def _get_cita(self, id_cita: int) -> Cita:
        cita = self.citas.get_by_id(id_cita)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada.",
            )
        return cita

    def list(
        self,
        paciente_id: Optional[int] = None,
        medico_id: Optional[int] = None,
    ) -> List[dict[str, Any]]:
        citas = self.citas.list(paciente_id=paciente_id, medico_id=medico_id)
        return [self._build_cita_data(cita) for cita in citas]

    def get_by_user(self, usuario: Usuario) -> List[dict[str, Any]]:
        if usuario.rol == RolUsuario.paciente:
            return self.list(paciente_id=usuario.id_usuario)
        if usuario.rol == RolUsuario.medico:
            medico = self.medicos.get_by_usuario_id(usuario.id_usuario)
            if not medico:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medico no encontrado.",
                )
            return self.list(medico_id=medico.id_medico)
        return self.list()

    def get(self, id_cita: int) -> dict[str, Any]:
        return self._build_cita_data(self._get_cita(id_cita))

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

    def create(self, cita_in: CitaCreate) -> dict[str, Any]:
        self._validar_paciente(cita_in.id_paciente)
        self._validar_medico(cita_in.id_medico)

        estado = cita_in.estado or EstadoCita.pendiente
        cita = Cita(
            id_paciente=cita_in.id_paciente,
            id_medico=cita_in.id_medico,
            fecha=cita_in.fecha,
            hora=cita_in.hora,
            estado=estado,
        )
        return self._build_cita_data(self.citas.create(cita))

    def update(self, id_cita: int, cita_in: CitaUpdate) -> dict[str, Any]:
        cita = self._get_cita(id_cita)
        data = remove_none(schema_to_dict(cita_in))
        if not data:
            return self._build_cita_data(cita)

        if "id_paciente" in data:
            self._validar_paciente(data["id_paciente"])
        if "id_medico" in data:
            self._validar_medico(data["id_medico"])

        previous_estado = cita.estado
        updated = self.citas.update(cita, data)
        new_estado = data.get("estado")
        if new_estado is not None and self._estado_value(new_estado) != self._estado_value(previous_estado):
            self._notify_estado_cita(updated)

        return self._build_cita_data(updated)

    def delete(self, id_cita: int) -> None:
        cita = self._get_cita(id_cita)
        self.citas.delete(cita)

    def _notify_estado_cita(self, cita: Cita) -> None:
        if cita.estado not in (EstadoCita.confirmada, EstadoCita.rechazada):
            return

        paciente = cita.paciente or self.usuarios.get_by_id(cita.id_paciente)
        if not paciente or not paciente.correo:
            return

        medico = cita.medico or self.medicos.get_by_id(cita.id_medico)
        medico_nombre = ""
        especialidad = ""
        if medico and medico.usuario:
            medico_nombre = medico.usuario.nombre
        if medico and medico.especialidad:
            especialidad = medico.especialidad.nombre

        try:
            send_cita_estado_email(
                to_email=paciente.correo,
                paciente_nombre=paciente.nombre,
                medico_nombre=medico_nombre or "Medico",
                especialidad=especialidad,
                fecha=cita.fecha,
                hora=cita.hora,
                estado=cita.estado,
            )
        except Exception:
            logger.exception(
                "Error sending status email for cita %s", cita.id_cita
            )

    @staticmethod
    def _estado_value(estado: object) -> str:
        return str(getattr(estado, "value", estado))
