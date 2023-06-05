from typing import List
from pydantic import Field
from app.data_transfer_objects.dto_order import DtoOrder
from app.data_transfer_objects.dto_security_price import DtoSecurityPrice
from core.data_transfer_objects.dto_entity import DtoEntity


class DtoOrderInfo(DtoEntity):
    order: DtoOrder = Field(default_factory=None)
    security_prices: List[DtoSecurityPrice] = Field(default_factory=[])
