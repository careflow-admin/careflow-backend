from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.medicamento import Medicamento


class MedicamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Medicamento]:
        return self.db.query(Medicamento).all()

    def get_by_id(self, id_medicamento: int) -> Optional[Medicamento]:
        return (
            self.db.query(Medicamento)
            .filter(Medicamento.id_medicamento == id_medicamento)
            .first()
        )

    def get_by_nombre(self, nombre: str) -> Optional[Medicamento]:
        return self.db.query(Medicamento).filter(Medicamento.nombre == nombre).first()

    def create(self, medicamento: Medicamento) -> Medicamento:
        self.db.add(medicamento)
        self.db.commit()
        self.db.refresh(medicamento)
        return medicamento

    def update(self, medicamento: Medicamento, data: dict) -> Medicamento:
        for field, value in data.items():
            setattr(medicamento, field, value)
        self.db.commit()
        self.db.refresh(medicamento)
        return medicamento

    def delete(self, medicamento: Medicamento) -> None:
        self.db.delete(medicamento)
        self.db.commit()
