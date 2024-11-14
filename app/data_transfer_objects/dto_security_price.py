from typing import Optional

from pydantic import Field

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.security_price import SecurityPrice


class DtoSecurityPrice(DtoEntity):
    order_id: Optional[str] = Field(default=None)
    ticker: str
    price: Optional[float] = Field(default=None)

    def _is_identical_to_db_entity(self, entity: SecurityPrice) -> bool:
        return (
            super()._is_identical_to_db_entity(entity) and self.ticker == entity.ticker and self.price == entity.price
        )
