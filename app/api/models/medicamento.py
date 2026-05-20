from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.api.models.receta_medica import RecetaMedica
    from app.api.models.tipo_medicamento import TipoMedicamento


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    id_tipo_medicamento: Mapped[int] = mapped_column(
        ForeignKey("tipos_medicamento.id_tipo_medicamento"), nullable=False
    )
    dosis_recomendada: Mapped[str] = mapped_column(String(120), nullable=False)
    contraindicaciones: Mapped[str] = mapped_column(Text, nullable=False)

    tipo_medicamento: Mapped["TipoMedicamento"] = relationship(
        "TipoMedicamento", back_populates="medicamentos"
    )
    recetas: Mapped[list["RecetaMedica"]] = relationship(
        "RecetaMedica", back_populates="medicamento"
    )
