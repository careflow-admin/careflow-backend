from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.otp import OtpCodigo


class OtpRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, otp: OtpCodigo) -> OtpCodigo:
        self.db.add(otp)
        self.db.commit()
        self.db.refresh(otp)
        return otp

    def invalidate_for_usuario(self, id_usuario: int) -> int:
        updated = (
            self.db.query(OtpCodigo)
            .filter(OtpCodigo.id_usuario == id_usuario, OtpCodigo.usado.is_(False))
            .update({OtpCodigo.usado: True}, synchronize_session=False)
        )
        self.db.commit()
        return updated

    def get_active_by_codigo(
        self, id_usuario: int, codigo: str, now: datetime
    ) -> Optional[OtpCodigo]:
        return (
            self.db.query(OtpCodigo)
            .filter(
                OtpCodigo.id_usuario == id_usuario,
                OtpCodigo.codigo == codigo,
                OtpCodigo.usado.is_(False),
                OtpCodigo.expira_en >= now,
            )
            .order_by(OtpCodigo.creado_en.desc())
            .first()
        )

    def mark_used(self, otp: OtpCodigo) -> OtpCodigo:
        otp.usado = True
        self.db.commit()
        self.db.refresh(otp)
        return otp
