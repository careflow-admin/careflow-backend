from typing import Optional

from app.api.schemas.base import ORMBase


class MedicoBase(ORMBase):
    id_usuario: int
    especialidad_id: int

class UserInfo(ORMBase):
    nombre: str
    rol: str

class MedicoCreate(MedicoBase):
    pass

class MedicoRead(MedicoBase):
    id_medico: int

class MedicoData(MedicoBase):
    id_medico: int
    especialidad: str
    data: UserInfo

class MedicoUpdate(ORMBase):
    id_usuario: Optional[int] = None
    especialidad_id: Optional[int] = None
