from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.api.models.cita import Cita
from app.api.models.medico import Medico


class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        paciente_id: Optional[int] = None,
        medico_id: Optional[int] = None,
    ) -> list[Cita]:
        query = self.db.query(Cita).options(
            joinedload(Cita.medico).joinedload(Medico.usuario),
            joinedload(Cita.medico).joinedload(Medico.especialidad),
        )
        if paciente_id is not None:
            query = query.filter(Cita.id_paciente == paciente_id)
        if medico_id is not None:
            query = query.filter(Cita.id_medico == medico_id)
        return query.all()

    def get_by_id(self, id_cita: int) -> Optional[Cita]:
        return (
            self.db.query(Cita)
            .options(
                joinedload(Cita.medico).joinedload(Medico.usuario),
                joinedload(Cita.medico).joinedload(Medico.especialidad),
            )
            .filter(Cita.id_cita == id_cita)
            .first()
        )

    def create(self, cita: Cita) -> Cita:
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def update(self, cita: Cita, data: dict) -> Cita:
        for field, value in data.items():
            setattr(cita, field, value)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def delete(self, cita: Cita) -> None:
        self.db.delete(cita)
        self.db.commit()
