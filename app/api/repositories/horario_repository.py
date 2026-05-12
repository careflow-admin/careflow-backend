from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models.horario import Horario


class HorarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Horario]:
        return self.db.query(Horario).all()

    def list_by_medico(self, id_medico: int) -> List[Horario]:
        return self.db.query(Horario).filter(Horario.id_medico == id_medico).all()

    def get_by_id(self, id_horario: int) -> Optional[Horario]:
        return self.db.query(Horario).filter(Horario.id_horario == id_horario).first()

    def create(self, horario: Horario) -> Horario:
        self.db.add(horario)
        self.db.commit()
        self.db.refresh(horario)
        return horario

    def update(self, horario: Horario, data: dict) -> Horario:
        for field, value in data.items():
            setattr(horario, field, value)
        self.db.commit()
        self.db.refresh(horario)
        return horario

    def delete(self, horario: Horario) -> None:
        self.db.delete(horario)
        self.db.commit()
