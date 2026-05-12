from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.especialidad_repository import EspecialidadRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.medico import MedicoCreate, MedicoData, MedicoRead, MedicoUpdate
from app.api.services.medico_service import MedicoService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/medicos", tags=["Medicos"], dependencies=[Depends(get_current_user)]
)


def get_service(db: Session = Depends(get_db)) -> MedicoService:
    return MedicoService(
        medico_repo=MedicoRepository(db),
        usuario_repo=UsuarioRepository(db),
        especialidad_repo=EspecialidadRepository(db),
    )


@router.post("/", response_model=MedicoRead, status_code=status.HTTP_201_CREATED)
def crear_medico(
    medico_in: MedicoCreate, service: MedicoService = Depends(get_service)
):
    return service.create(medico_in)


@router.get("/", response_model=List[MedicoData])
def listar_medicos(service: MedicoService = Depends(get_service)):
    return service.list()


@router.get("/{id_medico}", response_model=MedicoData)
def obtener_medico(id_medico: int, service: MedicoService = Depends(get_service)):
    return service.get(id_medico)


@router.patch("/{id_medico}", response_model=MedicoRead)
def actualizar_medico(
    id_medico: int,
    service: MedicoService = Depends(get_service),
):
    return service.update(id_medico)


@router.delete("/{id_medico}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_medico(id_medico: int, service: MedicoService = Depends(get_service)):
    service.delete(id_medico)
