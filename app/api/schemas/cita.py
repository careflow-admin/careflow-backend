from datetime import date, time
from typing import Optional

from app.api.models.cita import EstadoCita
from app.api.schemas.base import ORMBase
from app.api.schemas.medico import MedicoData


class CitaBase(ORMBase):
    id_paciente: int
    id_medico: int
    fecha: date
    hora: time
    estado: EstadoCita


class CitaCreate(CitaBase):
    estado: Optional[EstadoCita] = None


class CitaRead(CitaBase):
    id_cita: int
    medico: MedicoData


class CitaUpdate(ORMBase):
    id_paciente: Optional[int] = None
    id_medico: Optional[int] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    estado: Optional[EstadoCita] = None
