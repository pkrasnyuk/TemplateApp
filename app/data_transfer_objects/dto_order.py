from datetime import datetime

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.order import Order


class DtoOrder(DtoEntity):
    label: str
    date: datetime

    def _is_identical_to_db_entity(self, entity: Order) -> bool:
        return (
            super()._is_identical_to_db_entity(entity)
            and self.label == entity.label
            and self.date.date() == entity.date.date()
        )
