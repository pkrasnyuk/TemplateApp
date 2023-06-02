from datetime import datetime
from typing import Optional

from pydantic import Field

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.security_price import SecurityPrice


class DtoSecurityPrice(DtoEntity):
    date: datetime
    ticker: Optional[str] = Field(default_factory=None)
    price: Optional[float] = Field(default_factory=None)

    def _is_identical_to_db_entity(self, entity: SecurityPrice) -> bool:
        return (
            super()._is_identical_to_db_entity(entity)
            and self.date == entity.date
            and self.ticker == entity.ticker
            and self.price == entity.price
        )
