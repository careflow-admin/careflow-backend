from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.especialidad_repository import EspecialidadRepository
from app.api.schemas.especialidad import (
    EspecialidadCreate,
    EspecialidadRead,
    EspecialidadUpdate,
)
from app.api.services.especialidad_service import EspecialidadService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"],
    dependencies=[Depends(get_current_user)],
)


def get_service(db: Session = Depends(get_db)) -> EspecialidadService:
    return EspecialidadService(EspecialidadRepository(db))


@router.post("/", response_model=EspecialidadRead, status_code=status.HTTP_201_CREATED)
def crear_especialidad(
    especialidad_in: EspecialidadCreate,
    service: EspecialidadService = Depends(get_service),
):
    return service.create(especialidad_in)


@router.get("/", response_model=List[EspecialidadRead])
def listar_especialidades(service: EspecialidadService = Depends(get_service)):
    return service.list()


@router.get("/{id_especialidad}", response_model=EspecialidadRead)
def obtener_especialidad(
    id_especialidad: int, service: EspecialidadService = Depends(get_service)
):
    return service.get(id_especialidad)


@router.patch("/{id_especialidad}", response_model=EspecialidadRead)
def actualizar_especialidad(
    id_especialidad: int,
    especialidad_in: EspecialidadUpdate,
    service: EspecialidadService = Depends(get_service),
):
    return service.update(id_especialidad, especialidad_in)


@router.delete("/{id_especialidad}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_especialidad(
    id_especialidad: int, service: EspecialidadService = Depends(get_service)
):
    service.delete(id_especialidad)
