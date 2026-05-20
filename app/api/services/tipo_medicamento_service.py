from fastapi import HTTPException, status

from app.api.models.tipo_medicamento import TipoMedicamento
from app.api.repositories.tipo_medicamento_repository import TipoMedicamentoRepository
from app.api.schemas.tipo_medicamento import TipoMedicamentoCreate, TipoMedicamentoUpdate
from app.api.services.base import remove_none, schema_to_dict


class TipoMedicamentoService:
    def __init__(self, repo: TipoMedicamentoRepository):
        self.repo = repo

    def list(self) -> list[TipoMedicamento]:
        return self.repo.list()

    def get(self, id_tipo_medicamento: int) -> TipoMedicamento:
        tipo = self.repo.get_by_id(id_tipo_medicamento)
        if not tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de medicamento no encontrado.",
            )
        return tipo

    def create(self, tipo_in: TipoMedicamentoCreate) -> TipoMedicamento:
        existente = self.repo.get_by_nombre(tipo_in.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de medicamento ya registrado.",
            )

        tipo = TipoMedicamento(nombre=tipo_in.nombre)
        return self.repo.create(tipo)

    def update(
        self, id_tipo_medicamento: int, tipo_in: TipoMedicamentoUpdate
    ) -> TipoMedicamento:
        tipo = self.get(id_tipo_medicamento)
        data = remove_none(schema_to_dict(tipo_in))
        if not data:
            return tipo

        if "nombre" in data and data["nombre"] != tipo.nombre:
            existente = self.repo.get_by_nombre(data["nombre"])
            if existente and existente.id_tipo_medicamento != tipo.id_tipo_medicamento:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tipo de medicamento ya registrado.",
                )

        return self.repo.update(tipo, data)

    def delete(self, id_tipo_medicamento: int) -> None:
        tipo = self.get(id_tipo_medicamento)
        self.repo.delete(tipo)
