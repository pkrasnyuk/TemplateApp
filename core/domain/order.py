from datetime import datetime

from core.domain.mongo_entity import MongoEntity


class Order(MongoEntity):
    label: str
    date: datetime
