from pydantic import BaseConfig, BaseModel
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class DbEntity(DeclarativeBase):
    pass


class Entity(BaseModel):
    id: int

    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        require_by_default = False
        orm_mode = True
