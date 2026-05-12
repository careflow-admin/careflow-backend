from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.horario_repository import HorarioRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.schemas.horario import HorarioCreate, HorarioRead, HorarioUpdate
from app.api.services.horario_service import HorarioService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/horarios", tags=["Horarios"], dependencies=[Depends(get_current_user)]
)


def get_service(db: Session = Depends(get_db)) -> HorarioService:
    return HorarioService(
        horario_repo=HorarioRepository(db),
        medico_repo=MedicoRepository(db),
    )


@router.post("/", response_model=HorarioRead, status_code=status.HTTP_201_CREATED)
def crear_horario(
    horario_in: HorarioCreate, service: HorarioService = Depends(get_service)
):
    return service.create(horario_in)


@router.get("/", response_model=List[HorarioRead])
def listar_horarios(service: HorarioService = Depends(get_service)):
    return service.list()


@router.get("/medico/{id_medico}/disponibilidad", response_model=List[HorarioRead])
def disponibilidad(id_medico: int, service: HorarioService = Depends(get_service)):
    return service.get_disponibilidad(id_medico)


@router.get("/{id_horario}", response_model=HorarioRead)
def obtener_horario(id_horario: int, service: HorarioService = Depends(get_service)):
    return service.get(id_horario)


@router.patch("/{id_horario}", response_model=HorarioRead)
def actualizar_horario(
    id_horario: int,
    horario_in: HorarioUpdate,
    service: HorarioService = Depends(get_service),
):
    return service.update(id_horario, horario_in)


@router.delete("/{id_horario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_horario(id_horario: int, service: HorarioService = Depends(get_service)):
    service.delete(id_horario)
