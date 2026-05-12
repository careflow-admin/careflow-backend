from pydantic import BaseModel

try:
    from pydantic import ConfigDict
except ImportError:  # Pydantic v1
    ConfigDict = None


class ORMBase(BaseModel):
    if ConfigDict:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True
