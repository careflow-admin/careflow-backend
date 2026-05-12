from datetime import time
from typing import Optional

from app.api.models.horario import DiaSemana
from app.api.schemas.base import ORMBase


class HorarioBase(ORMBase):
    id_medico: int
    dia: DiaSemana
    hora_inicio: time
    hora_fin: time


class HorarioCreate(HorarioBase):
    pass


class HorarioRead(HorarioBase):
    id_horario: int


class HorarioUpdate(ORMBase):
    id_medico: Optional[int] = None
    dia: Optional[DiaSemana] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
