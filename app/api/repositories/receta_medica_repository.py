from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models.receta_medica import RecetaMedica


class RecetaMedicaRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[RecetaMedica]:
        return self.db.query(RecetaMedica).all()

    def list_by_historial(self, id_historial: int) -> List[RecetaMedica]:
        return (
            self.db.query(RecetaMedica)
            .filter(RecetaMedica.id_historial == id_historial)
            .all()
        )

    def get_by_id(self, id_receta: int) -> Optional[RecetaMedica]:
        return (
            self.db.query(RecetaMedica)
            .filter(RecetaMedica.id_receta == id_receta)
            .first()
        )

    def create(self, receta: RecetaMedica) -> RecetaMedica:
        self.db.add(receta)
        self.db.commit()
        self.db.refresh(receta)
        return receta

    def update(self, receta: RecetaMedica, data: dict) -> RecetaMedica:
        for field, value in data.items():
            setattr(receta, field, value)
        self.db.commit()
        self.db.refresh(receta)
        return receta

    def delete(self, receta: RecetaMedica) -> None:
        self.db.delete(receta)
        self.db.commit()
