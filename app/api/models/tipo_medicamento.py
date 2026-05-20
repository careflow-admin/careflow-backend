from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.api.models.medicamento import Medicamento


class TipoMedicamento(Base):
    __tablename__ = "tipos_medicamento"

    id_tipo_medicamento: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    medicamentos: Mapped[list["Medicamento"]] = relationship(
        "Medicamento", back_populates="tipo_medicamento"
    )
