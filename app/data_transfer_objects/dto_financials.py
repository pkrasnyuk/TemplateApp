from datetime import datetime
from typing import Optional

from pydantic import Field

from app.data_transfer_objects.dto_derived_financials import DtoDerivedFinancials
from app.data_transfer_objects.dto_entity import DtoEntity
from app.domain.enums import FinancialsType
from app.domain.financials import DbFinancials
from app.helpers.common import value2str


class DtoFinancials(DtoEntity):
    type: FinancialsType = Field(max_length=1)
    dt: datetime
    label: str = Field(max_length=16)
    price: Optional[float] = Field(default=None)
    dto_derived_financials: Optional[DtoDerivedFinancials] = Field(default=None)

    def __repr__(self):
        return f"DtoFinancials({self.type} - {value2str(self.dt)} - {self.label})"

    def __hash__(self):
        return hash((self.type, self.dt, self.label))

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return NotImplemented
        return self.type == other.type and self.dt == other.dt and self.label == other.label

    def _is_identical_to_db_entity(self, entity: DbFinancials) -> bool:
        return (
            super()._is_identical_to_db_entity(entity)
            and self.type == entity.type
            and self.dt.date() == entity.dt
            and self.label == entity.label
            and self.price == entity.price
        )
