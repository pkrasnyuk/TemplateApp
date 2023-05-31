from datetime import datetime
from typing import Optional

from core.domain.mongo_entity import MongoEntity


class SecurityPrice(MongoEntity):
    date: datetime
    ticker: Optional[str] = None
    price: Optional[float] = None
