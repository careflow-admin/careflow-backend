from __future__ import annotations

import enum
from datetime import date, time

from sqlalchemy import Date, Enum, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from app.api.models.usuario import Usuario
from app.api.models.medico import Medico


class EstadoCita(str, enum.Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    cancelada = "cancelada"
    rechazada = "rechazada"


class Cita(Base):
    __tablename__ = "citas"

    id_cita: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_paciente: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_medico: Mapped[int] = mapped_column(
        ForeignKey("medicos.id_medico"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora: Mapped[time] = mapped_column(Time, nullable=False)
    estado: Mapped[EstadoCita] = mapped_column(
        Enum(EstadoCita), nullable=False, default=EstadoCita.pendiente
    )

    paciente: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="citas_paciente", foreign_keys="Cita.id_paciente"
    )
    medico: Mapped["Medico"] = relationship("Medico", back_populates="citas")
