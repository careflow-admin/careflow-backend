from typing import Optional

from sqlalchemy.orm import Session, selectinload

from app.api.models.historial_clinico import HistorialClinico


class HistorialClinicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        paciente_id: Optional[int] = None,
        medico_id: Optional[int] = None,
    ) -> list[HistorialClinico]:
        query = self.db.query(HistorialClinico).options(
            selectinload(HistorialClinico.recetas)
        )
        if paciente_id is not None:
            query = query.filter(HistorialClinico.id_paciente == paciente_id)
        if medico_id is not None:
            query = query.filter(HistorialClinico.id_medico == medico_id)
        return query.all()

    def get_by_id(self, id_historial: int) -> Optional[HistorialClinico]:
        return (
            self.db.query(HistorialClinico)
            .options(selectinload(HistorialClinico.recetas))
            .filter(HistorialClinico.id_historial == id_historial)
            .first()
        )

    def create(self, historial: HistorialClinico) -> HistorialClinico:
        self.db.add(historial)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def update(self, historial: HistorialClinico, data: dict) -> HistorialClinico:
        for field, value in data.items():
            setattr(historial, field, value)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def delete(self, historial: HistorialClinico) -> None:
        self.db.delete(historial)
        self.db.commit()
