from datetime import datetime, timedelta
import secrets

from fastapi import HTTPException, status

from app.api.models.otp import OtpCodigo
from app.api.models.usuario import Usuario
from app.api.repositories.otp_repository import OtpRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.security.passwords import hash_password, verify_password
from app.utils.email import send_otp_email


class AuthService:
    OTP_TTL_MINUTES = 10

    def __init__(self, usuario_repo: UsuarioRepository, otp_repo: OtpRepository):
        self.usuarios = usuario_repo
        self.otps = otp_repo

    def login(self, identificacion: str, contrasena: str) -> Usuario:
        usuario = self._get_usuario(identificacion)
        if not usuario.contrasena_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario sin contrasena. Complete el registro.",
            )
        if not verify_password(contrasena, usuario.contrasena_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contrasena incorrecta.",
            )
        return usuario

    def iniciar_registro(self, identificacion: str) -> tuple[str, datetime]:
        usuario = self._get_usuario(identificacion)
        if usuario.contrasena_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario ya tiene contrasena.",
            )

        now = datetime.utcnow()
        expira_en = now + timedelta(minutes=self.OTP_TTL_MINUTES)
        self.otps.invalidate_for_usuario(usuario.id_usuario)
        codigo = self._generar_codigo()

        otp = OtpCodigo(
            id_usuario=usuario.id_usuario,
            codigo=codigo,
            creado_en=now,
            expira_en=expira_en,
            usado=False,
        )
        self.otps.create(otp)
        send_otp_email(usuario.correo, codigo)
        return usuario.correo, expira_en

    def validar_identificacion(self, identificacion: str) -> str:
        usuario = self._get_usuario(identificacion)
        if usuario.contrasena_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario ya tiene contrasena.",
            )
        return usuario.correo

    def verificar_otp(self, identificacion: str, codigo: str) -> tuple[Usuario, datetime]:
        usuario = self._get_usuario(identificacion)
        otp = self._get_otp_valido(usuario, codigo)
        return usuario, otp.expira_en

    def set_password(self, identificacion: str, codigo: str, contrasena: str) -> None:
        usuario = self._get_usuario(identificacion)
        if usuario.contrasena_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario ya tiene contrasena.",
            )

        otp = self._get_otp_valido(usuario, codigo)

        self.usuarios.update(usuario, {"contrasena_hash": hash_password(contrasena)})
        self.otps.mark_used(otp)

    def _get_usuario(self, identificacion: str) -> Usuario:
        usuario = self.usuarios.get_by_identificacion(identificacion)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado.",
            )
        return usuario

    def _get_otp_valido(self, usuario: Usuario, codigo: str) -> OtpCodigo:
        otp = self.otps.get_active_by_codigo(usuario.id_usuario, codigo, datetime.utcnow())
        if not otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Codigo OTP invalido o vencido.",
            )
        return otp

    def _generar_codigo(self, length: int = 6) -> str:
        return "".join(secrets.choice("0123456789") for _ in range(length))
