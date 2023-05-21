from pydantic import Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.domain.entity import DbEntity, Entity


class DbCompany(DbEntity):
    __tablename__ = "Company"

    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(length=128), index=True)
    analyst = Column("Analyst", String(length=64))

    financials = relationship("DbFinancials", back_populates="company", lazy=True)  # type: ignore

    def __repr__(self):
        return self.name


class Company(Entity):
    name: str = Field(max_length=128)
    analyst: str = Field(max_length=64)
