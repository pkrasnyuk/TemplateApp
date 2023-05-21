from typing import List

from pydantic import Field

from app.data_transfer_objects.dto_entity import DtoEntity
from app.data_transfer_objects.dto_financials import DtoFinancials
from app.domain.company import DbCompany


class DtoCompany(DtoEntity):
    name: str = Field(max_length=128)
    analyst: str = Field(max_length=64)
    dto_financials: List[DtoFinancials] = Field(default=[])

    def __repr__(self):
        return f"DtoCompany({self.name})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return NotImplemented
        return self.name == other.name

    def _is_identical_to_db_entity(self, entity: DbCompany) -> bool:
        return (
            super()._is_identical_to_db_entity(entity) and self.name == entity.name and self.analyst == entity.analyst
        )
