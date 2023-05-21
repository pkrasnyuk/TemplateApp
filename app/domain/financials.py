from datetime import datetime
from typing import Optional

from pydantic import Field
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.mssql import DATETIMEOFFSET
from sqlalchemy.orm import relationship

from app.domain.entity import DbEntity, Entity
from app.domain.enums import FinancialsType


class DbFinancials(DbEntity):
    __tablename__ = "Financials"

    id = Column("Id", Integer, primary_key=True, index=True)
    type = Column("Type", String(length=1))
    dt = Column("Date", DateTime)
    label = Column("Label", String(length=16))
    company_id = Column("CompanyId", Integer, ForeignKey("Company.Id"))
    last_updated = Column("LastUpdated", DATETIMEOFFSET)
    price = Column("Price", Float, nullable=True)

    company = relationship("DbCompany", back_populates="financials")  # type: ignore


class Financials(Entity):
    type: FinancialsType = Field(max_length=1)
    dt: datetime
    label: str = Field(max_length=16)
    company_id: int
    last_updated: datetime
    price: Optional[float] = Field(default=None)
