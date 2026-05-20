from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.historial_clinico_repository import HistorialClinicoRepository
from app.api.repositories.medico_repository import MedicoRepository
from app.api.repositories.usuario_repository import UsuarioRepository
from app.api.schemas.historial_clinico import (
    HistorialClinicoCreate,
    HistorialClinicoRead,
    HistorialClinicoUpdate,
)
from app.api.services.historial_clinico_service import HistorialClinicoService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/historiales-clinicos",
    tags=["Historiales Clinicos"],
    dependencies=[Depends(get_current_user)],
)


def get_service(db: Session = Depends(get_db)) -> HistorialClinicoService:
    return HistorialClinicoService(
        historial_repo=HistorialClinicoRepository(db),
        usuario_repo=UsuarioRepository(db),
        medico_repo=MedicoRepository(db),
    )


@router.post("/", response_model=HistorialClinicoRead, status_code=status.HTTP_201_CREATED)
def crear_historial(
    historial_in: HistorialClinicoCreate,
    service: HistorialClinicoService = Depends(get_service),
):
    return service.create(historial_in)


@router.get("/", response_model=List[HistorialClinicoRead])
def listar_historiales(
    paciente_id: Optional[int] = None,
    medico_id: Optional[int] = None,
    service: HistorialClinicoService = Depends(get_service),
):
    return service.list(paciente_id=paciente_id, medico_id=medico_id)


@router.get("/{id_historial}", response_model=HistorialClinicoRead)
def obtener_historial(
    id_historial: int, service: HistorialClinicoService = Depends(get_service)
):
    return service.get(id_historial)


@router.patch("/{id_historial}", response_model=HistorialClinicoRead)
def actualizar_historial(
    id_historial: int,
    historial_in: HistorialClinicoUpdate,
    service: HistorialClinicoService = Depends(get_service),
):
    return service.update(id_historial, historial_in)


@router.delete("/{id_historial}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_historial(
    id_historial: int, service: HistorialClinicoService = Depends(get_service)
):
    service.delete(id_historial)
