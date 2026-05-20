from datetime import datetime
from typing import Optional

from pydantic import Field

from app.api.schemas.base import ORMBase
from app.api.schemas.receta_medica import RecetaMedicaRead


class HistorialClinicoBase(ORMBase):
    id_paciente: int
    id_medico: int
    motivo: str = Field(..., max_length=50)
    diagnostico: str
    sintomas: str
    observaciones: str
    tratamiento: str


class HistorialClinicoCreate(HistorialClinicoBase):
    pass


class HistorialClinicoRead(HistorialClinicoBase):
    id_historial: int
    fecha_creacion: datetime
    ultima_actualizacion: datetime
    recetas: list[RecetaMedicaRead] = []


class HistorialClinicoUpdate(ORMBase):
    id_paciente: Optional[int] = None
    id_medico: Optional[int] = None
    motivo: Optional[str] = Field(default=None, max_length=50)
    diagnostico: Optional[str] = None
    sintomas: Optional[str] = None
    observaciones: Optional[str] = None
    tratamiento: Optional[str] = None
