from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.medicamento_repository import MedicamentoRepository
from app.api.schemas.medicamento import (
    MedicamentoCreate,
    MedicamentoData,
    MedicamentoRead,
    MedicamentoUpdate,
)
from app.api.services.medicamento_service import MedicamentoService
from app.api.repositories.tipo_medicamento_repository import TipoMedicamentoRepository
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/medicamentos", tags=["Medicamentos"], dependencies=[Depends(get_current_user)]
)


def get_service(db: Session = Depends(get_db)) -> MedicamentoService:
    return MedicamentoService(
        MedicamentoRepository(db),
        TipoMedicamentoRepository(db),
    )


@router.post("/", response_model=MedicamentoRead, status_code=status.HTTP_201_CREATED)
def crear_medicamento(
    medicamento_in: MedicamentoCreate, service: MedicamentoService = Depends(get_service)
):
    return service.create(medicamento_in)


@router.get("/", response_model=List[MedicamentoData])
def listar_medicamentos(service: MedicamentoService = Depends(get_service)):
    return service.list()


@router.get("/{id_medicamento}", response_model=MedicamentoData)
def obtener_medicamento(
    id_medicamento: int, service: MedicamentoService = Depends(get_service)
):
    return service.get(id_medicamento)


@router.patch("/{id_medicamento}", response_model=MedicamentoRead)
def actualizar_medicamento(
    id_medicamento: int,
    medicamento_in: MedicamentoUpdate,
    service: MedicamentoService = Depends(get_service),
):
    return service.update(id_medicamento, medicamento_in)


@router.delete("/{id_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_medicamento(
    id_medicamento: int, service: MedicamentoService = Depends(get_service)
):
    service.delete(id_medicamento)
