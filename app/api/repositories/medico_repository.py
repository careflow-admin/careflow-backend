from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.medico import Medico


class MedicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Medico]:
        return self.db.query(Medico).all()

    def get_by_id(self, id_medico: int) -> Optional[Medico]:
        return self.db.query(Medico).filter(Medico.id_medico == id_medico).first()

    def get_by_usuario_id(self, id_usuario: int) -> Optional[Medico]:
        return self.db.query(Medico).filter(Medico.id_usuario == id_usuario).first()

    def create(self, medico: Medico) -> Medico:
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def update(self, medico: Medico, data: dict) -> Medico:
        for field, value in data.items():
            setattr(medico, field, value)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def delete(self, medico: Medico) -> None:
        self.db.delete(medico)
        self.db.commit()
