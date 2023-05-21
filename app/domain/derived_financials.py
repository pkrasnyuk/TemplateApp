from typing import Optional

from pydantic import Field
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import backref, relationship

from app.domain.entity import DbEntity, Entity
from app.domain.financials import DbFinancials


class DbDerivedFinancials(DbEntity):
    __tablename__ = "DerivedFinancials"

    id = Column("Id", Integer, ForeignKey("Financials.Id"), primary_key=True, index=True)
    total_profit = Column("TotalProfit", Float, nullable=True)
    total_price = Column("TotalPrice", Float, nullable=True)

    financials = relationship(DbFinancials, backref=backref("DerivedFinancials", uselist=False))


class DerivedFinancials(Entity):
    total_profit: Optional[float] = Field(default=None)
    total_price: Optional[float] = Field(default=None)
