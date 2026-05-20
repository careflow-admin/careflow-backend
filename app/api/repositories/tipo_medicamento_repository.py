from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.tipo_medicamento import TipoMedicamento


class TipoMedicamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[TipoMedicamento]:
        return self.db.query(TipoMedicamento).all()

    def get_by_id(self, id_tipo_medicamento: int) -> Optional[TipoMedicamento]:
        return (
            self.db.query(TipoMedicamento)
            .filter(TipoMedicamento.id_tipo_medicamento == id_tipo_medicamento)
            .first()
        )

    def get_by_nombre(self, nombre: str) -> Optional[TipoMedicamento]:
        return self.db.query(TipoMedicamento).filter(TipoMedicamento.nombre == nombre).first()

    def create(self, tipo: TipoMedicamento) -> TipoMedicamento:
        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def update(self, tipo: TipoMedicamento, data: dict) -> TipoMedicamento:
        for field, value in data.items():
            setattr(tipo, field, value)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def delete(self, tipo: TipoMedicamento) -> None:
        self.db.delete(tipo)
        self.db.commit()
