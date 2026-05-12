from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Usuario]:
        return self.db.query(Usuario).all()

    def get_by_id(self, id_usuario: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    def get_by_identificacion(self, identificacion: str) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(Usuario.identificacion == identificacion)
            .first()
        )

    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario, data: dict) -> Usuario:
        for field, value in data.items():
            setattr(usuario, field, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> None:
        self.db.delete(usuario)
        self.db.commit()
