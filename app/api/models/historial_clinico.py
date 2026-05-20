from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.api.models.usuario import Usuario
    from app.api.models.medico import Medico
    from app.api.models.receta_medica import RecetaMedica


class HistorialClinico(Base):
    __tablename__ = "historial_clinico"

    id_historial: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_paciente: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_medico: Mapped[int] = mapped_column(
        ForeignKey("medicos.id_medico"), nullable=False
    )
    motivo: Mapped[str] = mapped_column(String(50), nullable=False)
    diagnostico: Mapped[str] = mapped_column(Text, nullable=False)
    sintomas: Mapped[str] = mapped_column(Text, nullable=False)
    observaciones: Mapped[str] = mapped_column(Text, nullable=False)
    tratamiento: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    ultima_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    paciente: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="historiales_paciente",
        foreign_keys="HistorialClinico.id_paciente",
    )
    medico: Mapped["Medico"] = relationship(
        "Medico",
        back_populates="historiales",
    )
    recetas: Mapped[list["RecetaMedica"]] = relationship(
        "RecetaMedica",
        back_populates="historial",
    )
