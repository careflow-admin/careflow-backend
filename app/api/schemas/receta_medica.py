from typing import Optional

from app.api.schemas.base import ORMBase


class RecetaMedicaBase(ORMBase):
    id_historial: int
    id_medicamento: int
    dosis: str
    frecuencia: str
    duracion: str
    indicaciones: str


class RecetaMedicaCreate(RecetaMedicaBase):
    pass


class RecetaMedicaRead(RecetaMedicaBase):
    id_receta: int


class RecetaMedicaUpdate(ORMBase):
    id_historial: Optional[int] = None
    id_medicamento: Optional[int] = None
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    duracion: Optional[str] = None
    indicaciones: Optional[str] = None
