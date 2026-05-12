from __future__ import annotations

import enum
from datetime import time

from sqlalchemy import Enum, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from app.api.models.medico import Medico

class DiaSemana(str, enum.Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"


class Horario(Base):
    __tablename__ = "horarios"

    id_horario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_medico: Mapped[int] = mapped_column(
        ForeignKey("medicos.id_medico"), nullable=False
    )
    dia: Mapped[DiaSemana] = mapped_column(Enum(DiaSemana), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)

    medico: Mapped["Medico"] = relationship("Medico", back_populates="horarios")
