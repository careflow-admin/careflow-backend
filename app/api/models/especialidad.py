from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from app.api.models.medico import Medico


class Especialidad(Base):
    __tablename__ = "especialidades"

    id_especialidad: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    medicos: Mapped[list["Medico"]] = relationship(
        "Medico", back_populates="especialidad"
    )
