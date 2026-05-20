from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.historial_clinico_repository import HistorialClinicoRepository
from app.api.repositories.medicamento_repository import MedicamentoRepository
from app.api.repositories.receta_medica_repository import RecetaMedicaRepository
from app.api.schemas.receta_medica import RecetaMedicaCreate, RecetaMedicaRead, RecetaMedicaUpdate
from app.api.services.receta_medica_service import RecetaMedicaService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/recetas-medicas",
    tags=["Recetas Medicas"],
    dependencies=[Depends(get_current_user)],
)


def get_service(db: Session = Depends(get_db)) -> RecetaMedicaService:
    return RecetaMedicaService(
        receta_repo=RecetaMedicaRepository(db),
        historial_repo=HistorialClinicoRepository(db),
        medicamento_repo=MedicamentoRepository(db),
    )


@router.post("/", response_model=RecetaMedicaRead, status_code=status.HTTP_201_CREATED)
def crear_receta(
    receta_in: RecetaMedicaCreate,
    service: RecetaMedicaService = Depends(get_service),
):
    return service.create(receta_in)


@router.get("/", response_model=List[RecetaMedicaRead])
def listar_recetas(
    id_historial: Optional[int] = None,
    service: RecetaMedicaService = Depends(get_service),
):
    return service.list(id_historial=id_historial)


@router.get("/{id_receta}", response_model=RecetaMedicaRead)
def obtener_receta(
    id_receta: int, service: RecetaMedicaService = Depends(get_service)
):
    return service.get(id_receta)


@router.patch("/{id_receta}", response_model=RecetaMedicaRead)
def actualizar_receta(
    id_receta: int,
    receta_in: RecetaMedicaUpdate,
    service: RecetaMedicaService = Depends(get_service),
):
    return service.update(id_receta, receta_in)


@router.delete("/{id_receta}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_receta(
    id_receta: int, service: RecetaMedicaService = Depends(get_service)
):
    service.delete(id_receta)
