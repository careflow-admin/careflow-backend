from typing import Optional

from app.api.schemas.base import ORMBase


class MedicamentoBase(ORMBase):
    nombre: str
    descripcion: str
    id_tipo_medicamento: int
    dosis_recomendada: str
    contraindicaciones: str


class MedicamentoCreate(MedicamentoBase):
    pass


class MedicamentoRead(MedicamentoBase):
    id_medicamento: int


class MedicamentoData(MedicamentoBase):
    id_medicamento: int
    tipo_medicamento: str


class MedicamentoUpdate(ORMBase):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tipo_medicamento: Optional[int] = None
    dosis_recomendada: Optional[str] = None
    contraindicaciones: Optional[str] = None
