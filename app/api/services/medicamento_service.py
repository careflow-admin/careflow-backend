from fastapi import HTTPException, status

from app.api.models.medicamento import Medicamento
from app.api.repositories.medicamento_repository import MedicamentoRepository
from app.api.repositories.tipo_medicamento_repository import TipoMedicamentoRepository
from app.api.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate
from app.api.services.base import remove_none, schema_to_dict


class MedicamentoService:
    def __init__(self, repo: MedicamentoRepository, tipo_repo: TipoMedicamentoRepository):
        self.repo = repo
        self.tipos = tipo_repo

    def _validar_tipo_medicamento(self, id_tipo_medicamento: int) -> None:
        tipo = self.tipos.get_by_id(id_tipo_medicamento)
        if not tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de medicamento no encontrado.",
            )

    def list(self) -> list[dict]:
        medicamentos = self.repo.list()
        return [
            {
                **medicamento.to_dict(),
                "tipo_medicamento": medicamento.tipo_medicamento.nombre,
            }
            for medicamento in medicamentos
        ]

    def get(self, id_medicamento: int) -> dict:
        medicamento = self.repo.get_by_id(id_medicamento)
        if not medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medicamento no encontrado.",
            )
        return {
            **medicamento.to_dict(),
            "tipo_medicamento": medicamento.tipo_medicamento.nombre,
        }

    def create(self, medicamento_in: MedicamentoCreate) -> Medicamento:
        existente = self.repo.get_by_nombre(medicamento_in.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Medicamento ya registrado.",
            )

        self._validar_tipo_medicamento(medicamento_in.id_tipo_medicamento)

        medicamento = Medicamento(
            nombre=medicamento_in.nombre,
            descripcion=medicamento_in.descripcion,
            id_tipo_medicamento=medicamento_in.id_tipo_medicamento,
            dosis_recomendada=medicamento_in.dosis_recomendada,
            contraindicaciones=medicamento_in.contraindicaciones,
        )
        return self.repo.create(medicamento)

    def update(
        self, id_medicamento: int, medicamento_in: MedicamentoUpdate
    ) -> Medicamento:
        medicamento = self.get(id_medicamento)
        data = remove_none(schema_to_dict(medicamento_in))
        if not data:
            return medicamento

        if "nombre" in data and data["nombre"] != medicamento.nombre:
            existente = self.repo.get_by_nombre(data["nombre"])
            if existente and existente.id_medicamento != medicamento.id_medicamento:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Medicamento ya registrado.",
                )

        if "id_tipo_medicamento" in data:
            self._validar_tipo_medicamento(data["id_tipo_medicamento"])

        return self.repo.update(medicamento, data)

    def delete(self, id_medicamento: int) -> None:
        medicamento = self.get(id_medicamento)
        self.repo.delete(medicamento)
