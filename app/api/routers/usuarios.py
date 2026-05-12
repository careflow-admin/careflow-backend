from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.api.services.usuario_service import UsuarioService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(get_current_user)]
)


def get_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(UsuarioRepository(db))


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_in: UsuarioCreate, service: UsuarioService = Depends(get_service)
):
    return service.create(usuario_in)


@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(service: UsuarioService = Depends(get_service)):
    return service.list()


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: int, service: UsuarioService = Depends(get_service)):
    return service.get(id_usuario)


@router.patch("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: int,
    usuario_in: UsuarioUpdate,
    service: UsuarioService = Depends(get_service),
):
    return service.update(id_usuario, usuario_in)


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int, service: UsuarioService = Depends(get_service)):
    service.delete(id_usuario)
