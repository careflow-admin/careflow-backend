from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.api.models.usuario import Usuario
    from app.api.models.cita import Cita
    from app.api.models.horario import Horario
    from app.api.models.especialidad import Especialidad
    from app.api.models.historial_clinico import HistorialClinico

class Medico(Base):
    __tablename__ = "medicos"

    id_medico: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), unique=True, nullable=False
    )
    especialidad_id: Mapped[int] = mapped_column(
        ForeignKey("especialidades.id_especialidad"), nullable=False
    )

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="medico")
    especialidad: Mapped["Especialidad"] = relationship(
        "Especialidad", back_populates="medicos"
    )
    citas: Mapped[list["Cita"]] = relationship("Cita", back_populates="medico")
    horarios: Mapped[list["Horario"]] = relationship(
        "Horario", back_populates="medico"
    )
    historiales: Mapped[list["HistorialClinico"]] = relationship(
        "HistorialClinico", back_populates="medico"
    )

    
