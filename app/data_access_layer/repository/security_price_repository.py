from datetime import datetime
from typing import List

from pymongo import MongoClient

from core.data_access_layer.repository.base_nosql_repository import BaseNoSqlRepository
from core.domain.security_price import SecurityPrice


class SecurityPriceRepository(BaseNoSqlRepository):
    def __init__(self, mongo_client: MongoClient, db_name: str):
        super().__init__(mongo_client=mongo_client, db_name=db_name, collection_name="SecurityPrice")
        self.entity = SecurityPrice

    def get_all(self):
        return self._get_collection()

    def get_by_id(self, id: str):
        return self._read_document_by_id(id)

    def get_between_dates(self, start: datetime, end: datetime):
        return self._read_documents({"date": {"$gte": start, "$lt": end}})

    def create(self, item: SecurityPrice):
        return self._insert_document(item)

    def insert_docs(self, items: List[SecurityPrice]):
        return self._insert_documents(items)

    def update(self, item: SecurityPrice):
        return self._update_document(item)

    def delete(self, id: str):
        self._delete_document(id)