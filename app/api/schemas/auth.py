from datetime import datetime

from app.api.schemas.base import ORMBase
from app.api.schemas.usuario import UsuarioRead


class AuthLoginRequest(ORMBase):
    identificacion: str
    contrasena: str


class AuthLoginResponse(ORMBase):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioRead


class OtpStartResponse(ORMBase):
    message: str
    correo: str
    expira_en: datetime


class OtpStartRequest(ORMBase):
    identificacion: str


class IdentificacionResponse(ORMBase):
    message: str
    correo: str


class OtpVerificarRequest(ORMBase):
    identificacion: str
    codigo: str


class OtpVerificarResponse(ORMBase):
    message: str
    expira_en: datetime
    access_token: str
    token_type: str = "bearer"


class OtpSetPasswordRequest(ORMBase):
    identificacion: str
    codigo: str
    contrasena: str


class OtpSetPasswordResponse(ORMBase):
    message: str
