from typing import Optional

from pydantic import Field

from core.domain.mongo_entity import MongoEntity
from core.domain.py_object_id import PyObjectId


class SecurityPrice(MongoEntity):
    order_id: Optional[PyObjectId] = Field(default=None)
    ticker: str
    price: Optional[float] = Field(default=None)
