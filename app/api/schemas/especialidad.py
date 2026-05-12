from typing import Optional

from app.api.schemas.base import ORMBase


class EspecialidadBase(ORMBase):
    nombre: str


class EspecialidadCreate(EspecialidadBase):
    pass


class EspecialidadRead(EspecialidadBase):
    id_especialidad: int


class EspecialidadUpdate(ORMBase):
    nombre: Optional[str] = None
