from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class DbEntity(DeclarativeBase):
    pass


class Entity(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, from_attributes=True)
    id: Optional[int]
