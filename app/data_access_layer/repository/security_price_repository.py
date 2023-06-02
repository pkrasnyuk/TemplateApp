import logging
from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, List, Optional

from automapper import mapper
from pymongo import MongoClient

from app.data_transfer_objects.dto_security_price import DtoSecurityPrice
from core.data_access_layer.repository.base_nosql_repository import BaseNoSqlRepository
from core.domain.security_price import SecurityPrice


class SecurityPriceRepository(BaseNoSqlRepository):
    def __init__(self, mongo_client: Callable[..., AbstractContextManager[MongoClient]], db_name: str):
        super().__init__(mongo_client=mongo_client, db_name=db_name, collection_name="SecurityPrice")
        self.entity = SecurityPrice
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_all(self) -> List[SecurityPrice]:
        return self._get_collection()

    def get_by_id(self, id: str) -> Optional[SecurityPrice]:
        return self._read_document_by_id(id)

    def get_between_dates(self, start: datetime, end: datetime) -> List[SecurityPrice]:
        return self._read_documents({"date": {"$gte": start, "$lt": end}})

    def create(self, item: SecurityPrice) -> Optional[SecurityPrice]:
        return self._insert_document(item)

    def insert_docs(self, items: List[SecurityPrice]) -> List[SecurityPrice]:
        return self._insert_documents(items)

    def update(self, item: SecurityPrice) -> Optional[SecurityPrice]:
        return self._update_document(item)

    def delete(self, id: str) -> None:
        self._delete_document(id)

    def bulk_save(self, items: List[DtoSecurityPrice]) -> None:
        if items is not None and len(items) > 0:
            security_prices: List[SecurityPrice] = self._get_collection()

            new_security_prices: List[SecurityPrice] = []
            existing_security_prices: List[SecurityPrice] = []
            removed_security_prices: List[int] = [x.id for x in security_prices]

            for item in items:
                if item is not None:
                    security_price: Optional[SecurityPrice] = next(
                        (x for x in security_prices if x.ticker == item.ticker),
                        None,
                    )
                    if security_price is None:
                        new_security_prices.append(mapper.to(SecurityPrice).map(item))
                    else:
                        if security_price.id in removed_security_prices:
                            removed_security_prices.remove(security_price.id)
                        if not item._is_identical_to_db_entity(entity=security_price):
                            existing_security_prices.append(
                                mapper.to(SecurityPrice).map(item, fields_mapping={"id": security_price.id})
                            )

            if len(removed_security_prices) > 0:
                delete_result = self.collection.delete_many({"_id": {"$in": removed_security_prices}})
                if delete_result is not None:
                    info_message: str = f"The {delete_result.deleted_count} security prices data from "
                    info_message += f"{len(removed_security_prices)} has deleted from database."
                    self.__logger.info(info_message)

            if len(new_security_prices) > 0:
                insert_result = self._insert_documents(docs=new_security_prices)
                if insert_result is not None:
                    info_message = f"The {len(insert_result)} security prices data from "
                    info_message += f"{len(new_security_prices)} has added to database."
                    self.__logger.info(info_message)

            if len(existing_security_prices) > 0:
                update_result = 0
                for existing_security_price in existing_security_prices:
                    self._update_document(doc=existing_security_price)
                    update_result += 1
                info_message = f"The {update_result} security prices data from "
                info_message += f"{len(existing_security_prices)} has updated in database."
                self.__logger.info(info_message)

        return None
