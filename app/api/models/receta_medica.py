from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.api.models.historial_clinico import HistorialClinico
    from app.api.models.medicamento import Medicamento


class RecetaMedica(Base):
    __tablename__ = "receta_medica"

    id_receta: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_historial: Mapped[int] = mapped_column(
        ForeignKey("historial_clinico.id_historial"), nullable=False
    )
    id_medicamento: Mapped[int] = mapped_column(
        ForeignKey("medicamentos.id_medicamento"), nullable=False
    )
    dosis: Mapped[str] = mapped_column(String(120), nullable=False)
    frecuencia: Mapped[str] = mapped_column(String(120), nullable=False)
    duracion: Mapped[str] = mapped_column(String(120), nullable=False)
    indicaciones: Mapped[str] = mapped_column(Text, nullable=False)

    historial: Mapped["HistorialClinico"] = relationship(
        "HistorialClinico", back_populates="recetas"
    )
    medicamento: Mapped["Medicamento"] = relationship(
        "Medicamento", back_populates="recetas"
    )
