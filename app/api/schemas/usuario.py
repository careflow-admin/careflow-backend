from typing import Optional

from pydantic import EmailStr

from app.api.models.usuario import RolUsuario
from app.api.schemas.base import ORMBase


class UsuarioBase(ORMBase):
    nombre: str
    correo: EmailStr
    rol: RolUsuario


class UsuarioCreate(UsuarioBase):
    contrasena: str


class UsuarioRead(UsuarioBase):
    id_usuario: int


class UsuarioMeRead(UsuarioRead):
    id_medico: Optional[int] = None


class UsuarioUpdate(ORMBase):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[RolUsuario] = None
    contrasena: Optional[str] = None
