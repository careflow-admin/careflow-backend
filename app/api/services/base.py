from typing import Any

from pydantic import BaseModel


def schema_to_dict(schema: BaseModel) -> dict[str, Any]:
    if hasattr(schema, "model_dump"):
        return schema.model_dump(exclude_unset=True)
    return schema.dict(exclude_unset=True)


def remove_none(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}
