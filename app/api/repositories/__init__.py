from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.especialidad_repository import EspecialidadRepository
from app.api.repositories.cita_repository import CitaRepository
from app.api.repositories.horario_repository import HorarioRepository
from app.api.repositories.otp_repository import OtpRepository

__all__ = [
    "UsuarioRepository",
    "MedicoRepository",
    "EspecialidadRepository",
    "CitaRepository",
    "HorarioRepository",
    "OtpRepository",
]
