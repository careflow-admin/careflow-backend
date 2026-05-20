from typing import Optional

from app.api.schemas.base import ORMBase


class TipoMedicamentoBase(ORMBase):
    nombre: str


class TipoMedicamentoCreate(TipoMedicamentoBase):
    pass


class TipoMedicamentoRead(TipoMedicamentoBase):
    id_tipo_medicamento: int


class TipoMedicamentoUpdate(ORMBase):
    nombre: Optional[str] = None
