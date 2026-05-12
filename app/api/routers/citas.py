from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.cita_repository import CitaRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.cita import CitaCreate, CitaRead, CitaUpdate
from app.api.services.cita_service import CitaService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/citas", tags=["Citas"], dependencies=[Depends(get_current_user)]
)


def get_service(db: Session = Depends(get_db)) -> CitaService:
    return CitaService(
        cita_repo=CitaRepository(db),
        usuario_repo=UsuarioRepository(db),
        medico_repo=MedicoRepository(db),
    )


@router.post("/", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(cita_in: CitaCreate, service: CitaService = Depends(get_service)):
    return service.create(cita_in)


@router.get("/", response_model=List[CitaRead])
def listar_citas(
    paciente_id: Optional[int] = None,
    medico_id: Optional[int] = None,
    service: CitaService = Depends(get_service),
):
    return service.list(paciente_id=paciente_id, medico_id=medico_id)


@router.get("/mis-citas", response_model=List[CitaRead])
def mis_citas(
    current_user=Depends(get_current_user),
    service: CitaService = Depends(get_service),
):
    return service.get_by_user(current_user)


@router.get("/{id_cita}", response_model=CitaRead)
def obtener_cita(id_cita: int, service: CitaService = Depends(get_service)):
    return service.get(id_cita)


@router.patch("/{id_cita}", response_model=CitaRead)
def actualizar_cita(
    id_cita: int,
    cita_in: CitaUpdate,
    service: CitaService = Depends(get_service),
):
    return service.update(id_cita, cita_in)


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: int, service: CitaService = Depends(get_service)):
    service.delete(id_cita)
