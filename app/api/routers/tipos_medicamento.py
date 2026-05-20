from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.repositories.tipo_medicamento_repository import TipoMedicamentoRepository
from app.api.schemas.tipo_medicamento import (
    TipoMedicamentoCreate,
    TipoMedicamentoRead,
    TipoMedicamentoUpdate,
)
from app.api.services.tipo_medicamento_service import TipoMedicamentoService
from app.database.session import get_db
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/tipos-medicamento",
    tags=["Tipos Medicamento"],
    dependencies=[Depends(get_current_user)],
)


def get_service(db: Session = Depends(get_db)) -> TipoMedicamentoService:
    return TipoMedicamentoService(TipoMedicamentoRepository(db))


@router.post("/", response_model=TipoMedicamentoRead, status_code=status.HTTP_201_CREATED)
def crear_tipo_medicamento(
    tipo_in: TipoMedicamentoCreate,
    service: TipoMedicamentoService = Depends(get_service),
):
    return service.create(tipo_in)


@router.get("/", response_model=List[TipoMedicamentoRead])
def listar_tipos_medicamento(service: TipoMedicamentoService = Depends(get_service)):
    return service.list()


@router.get("/{id_tipo_medicamento}", response_model=TipoMedicamentoRead)
def obtener_tipo_medicamento(
    id_tipo_medicamento: int, service: TipoMedicamentoService = Depends(get_service)
):
    return service.get(id_tipo_medicamento)


@router.patch("/{id_tipo_medicamento}", response_model=TipoMedicamentoRead)
def actualizar_tipo_medicamento(
    id_tipo_medicamento: int,
    tipo_in: TipoMedicamentoUpdate,
    service: TipoMedicamentoService = Depends(get_service),
):
    return service.update(id_tipo_medicamento, tipo_in)


@router.delete("/{id_tipo_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_medicamento(
    id_tipo_medicamento: int, service: TipoMedicamentoService = Depends(get_service)
):
    service.delete(id_tipo_medicamento)
