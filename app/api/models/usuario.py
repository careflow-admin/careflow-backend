from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.api.models.medico import Medico
    from app.api.models.cita import Cita

class RolUsuario(str, enum.Enum):
    paciente = "paciente"
    medico = "medico"
    admin = "admin"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    identificacion: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    correo: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario), nullable=False)

    medico: Mapped[Optional["Medico"]] = relationship(
        "Medico", back_populates="usuario", uselist=False
    )
    citas_paciente: Mapped[list["Cita"]] = relationship(
        "Cita", back_populates="paciente", foreign_keys="Cita.id_paciente"
    )
