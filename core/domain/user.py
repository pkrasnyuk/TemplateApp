from pydantic import Field, field_validator
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.domain.entity import DbEntity, Entity


class DbUser(DbEntity):
    __tablename__ = "User"

    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(length=32), index=True)
    api_key = Column("ApiKey", String(length=64), index=True)

    pricings = relationship("DbPricing", back_populates="user", lazy=True)  # type: ignore

    def __repr__(self):
        return self.name


class User(Entity):
    name: str = Field(max_length=32)
    api_key: str = Field(max_length=64)

    @field_validator("name", mode="after")
    def name_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v
