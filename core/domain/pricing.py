from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.mssql import DATETIMEOFFSET
from sqlalchemy.orm import relationship

from core.domain.entity import DbEntity, Entity
from core.domain.enums import RequestStatus


class DbPricing(DbEntity):
    __tablename__ = "Pricings"

    id = Column("Id", Integer, primary_key=True, index=True)
    ts = Column("TS", DATETIMEOFFSET)
    user_id = Column("UserId", Integer, ForeignKey("User.Id"))
    status = Column("Status", Integer)
    user_request_id = Column("UserRequestId", String(length=40))
    date = Column("Date", DateTime)
    level = Column("Level", Float)
    pricing = Column("Pricing", Float, default=0.0)

    user = relationship("DbUser", back_populates="pricings")  # type: ignore

    def __repr__(self):
        return str(self.id)


class Pricing(Entity):
    ts: datetime
    user_id: int
    status: RequestStatus
    user_request_id: UUID
    date: datetime
    level: float
    pricing: float = Field(ge=0.0, le=100.0)
