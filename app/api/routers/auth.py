from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.otp_repository import OtpRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.auth import (
    AuthLoginRequest,
    AuthLoginResponse,
    IdentificacionResponse,
    OtpStartRequest,
    OtpSetPasswordRequest,
    OtpSetPasswordResponse,
    OtpStartResponse,
    OtpVerificarRequest,
    OtpVerificarResponse,
)
from app.api.schemas.usuario import UsuarioMeRead
from app.api.services.auth_service import AuthService
from app.database.session import get_db
from app.api.models.usuario import RolUsuario
from app.security.auth import get_current_user
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UsuarioRepository(db), OtpRepository(db))

@router.post("/login", response_model=AuthLoginResponse)
def login(data: AuthLoginRequest, service: AuthService = Depends(get_service)):
    usuario = service.login(data.identificacion, data.contrasena)
    token = create_access_token(
        {"sub": str(usuario.id_usuario), "id_usuario": usuario.id_usuario}
    )
    return AuthLoginResponse(access_token=token, token_type="bearer", usuario=usuario)

@router.get("/me", response_model=UsuarioMeRead)
def get_me(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    id_medico = None
    if current_user.rol == RolUsuario.medico:
        medico = MedicoRepository(db).get_by_usuario_id(current_user.id_usuario)
        if medico:
            id_medico = medico.id_medico

    return UsuarioMeRead(
        id_usuario=current_user.id_usuario,
        nombre=current_user.nombre,
        correo=current_user.correo,
        rol=current_user.rol,
        id_medico=id_medico,
    )

@router.post("/registro/validar", response_model=IdentificacionResponse)
def validar_identificacion(
    data: OtpStartRequest,
    service: AuthService = Depends(get_service),
):
    correo = service.validar_identificacion(data.identificacion)
    return IdentificacionResponse(message="Identificacion valida.", correo=correo)

@router.post("/registro/consulta", response_model=OtpStartResponse)
def consulta_identificacion(
    data: OtpStartRequest,
    service: AuthService = Depends(get_service),
):
    correo, expira_en = service.iniciar_registro(data.identificacion)
    return OtpStartResponse(message="OTP enviado.", correo=correo, expira_en=expira_en)

@router.post("/otp/verificar", response_model=OtpVerificarResponse)
def verificar_otp(
    data: OtpVerificarRequest,
    service: AuthService = Depends(get_service),
):
    usuario, expira_en = service.verificar_otp(data.identificacion, data.codigo)
    token = create_access_token(
        {"sub": str(usuario.id_usuario), "id_usuario": usuario.id_usuario}
    )
    return OtpVerificarResponse(
        message="OTP valido.",
        expira_en=expira_en,
        access_token=token,
        token_type="bearer",
    )

@router.post("/otp/set-password", response_model=OtpSetPasswordResponse)
def set_password(
    data: OtpSetPasswordRequest,
    service: AuthService = Depends(get_service),
):
    service.set_password(data.identificacion, data.codigo, data.contrasena)
    return OtpSetPasswordResponse(message="Contrasena actualizada.")
