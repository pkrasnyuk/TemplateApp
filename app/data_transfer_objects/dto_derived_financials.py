from typing import Optional

from pydantic import Field

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.derived_financials import DbDerivedFinancials


class DtoDerivedFinancials(DtoEntity):
    total_profit: Optional[float] = Field(default=None)
    total_price: Optional[float] = Field(default=None)

    def _is_identical_to_db_entity(self, entity: DbDerivedFinancials) -> bool:
        return (
            super()._is_identical_to_db_entity(entity)
            and self.total_profit == entity.total_profit
            and self.total_price == entity.total_price
        )
