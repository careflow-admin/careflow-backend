from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.especialidad import Especialidad


class EspecialidadRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Especialidad]:
        return self.db.query(Especialidad).all()

    def get_by_id(self, id_especialidad: int) -> Optional[Especialidad]:
        return (
            self.db.query(Especialidad)
            .filter(Especialidad.id_especialidad == id_especialidad)
            .first()
        )

    def get_by_nombre(self, nombre: str) -> Optional[Especialidad]:
        return self.db.query(Especialidad).filter(Especialidad.nombre == nombre).first()

    def create(self, especialidad: Especialidad) -> Especialidad:
        self.db.add(especialidad)
        self.db.commit()
        self.db.refresh(especialidad)
        return especialidad

    def update(self, especialidad: Especialidad, data: dict) -> Especialidad:
        for field, value in data.items():
            setattr(especialidad, field, value)
        self.db.commit()
        self.db.refresh(especialidad)
        return especialidad

    def delete(self, especialidad: Especialidad) -> None:
        self.db.delete(especialidad)
        self.db.commit()
