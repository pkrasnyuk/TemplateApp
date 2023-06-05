import logging
from contextlib import AbstractContextManager
from datetime import datetime
from typing import Any, Callable, List, Optional

from automapper import mapper
from pymongo import MongoClient

from app.data_transfer_objects.dto_order_info import DtoOrderInfo
from core.data_access_layer.repository.base_nosql_repository import BaseNoSqlRepository
from core.domain.order import Order
from core.domain.py_object_id import PyObjectId
from core.domain.security_price import SecurityPrice


class SecurityPriceRepository(BaseNoSqlRepository):
    def __init__(self, mongo_client: Callable[..., AbstractContextManager[MongoClient]], db_name: str):
        super().__init__(mongo_client=mongo_client, db_name=db_name, collection_name="SecurityPrice")
        self.entity = SecurityPrice
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__db_name = db_name

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

    def __convert_many_orders(self, items: Any) -> List[Order]:
        result: List[Order] = []
        for item in items:
            entity: Optional[Order] = Order(**item) if item is not None else None
            if entity is not None:
                result.append(entity)
        return result

    def bulk_save(self, items: List[DtoOrderInfo]) -> None:
        with self._client() as db_client:
            db = db_client[self.__db_name]

            order_collection = db["Order"]
            security_price_collection = db["SecurityPrice"]

            orders: List[Order] = self.__convert_many_orders(items=order_collection.find())
            if items is not None and len(items) > 0:
                new_orders: List[Order] = []
                existing_orders: List[Order] = []
                removed_orders: List[PyObjectId] = [x.id for x in orders if x is not None]

                missed_security_prices: List[SecurityPrice] = []
                new_security_prices: List[tuple] = []
                existing_security_prices: List[SecurityPrice] = []
                removed_security_prices: List[PyObjectId] = []

                for item in items:
                    if item is not None and item.order is not None:
                        order: Optional[Order] = next(
                            (x for x in orders if x.label == item.order.label),
                            None,
                        )
                        if order is None:
                            new_order: Order = mapper.to(Order).map(item.order)
                            new_orders.append(new_order)
                            if item.security_prices is not None and len(item.security_prices) > 0:
                                for sprice in item.security_prices:
                                    if sprice is not None:
                                        new_security_prices.append((new_order, mapper.to(SecurityPrice).map(sprice)))
                        else:
                            removed_orders.remove(order.id)
                            security_prices: List[SecurityPrice] = self._convert_many(
                                items=security_price_collection.find({"order_id": order.id})
                            )
                            removed_security_prices.extend([x.id for x in security_prices if x is not None])
                            if not item.order._is_identical_to_db_entity(entity=order):
                                existing_orders.append(
                                    mapper.to(Order).map(item.order, fields_mapping={"id": order.id})
                                )
                            if item.security_prices is not None and len(item.security_prices) > 0:
                                for sprice in item.security_prices:
                                    if sprice is not None:
                                        security_price: Optional[SecurityPrice] = next(
                                            (
                                                x
                                                for x in security_prices
                                                if x.ticker == sprice.ticker and x.order_id == order.id
                                            ),
                                            None,
                                        )
                                        if security_price is None:
                                            missed_security_prices.append(
                                                mapper.to(SecurityPrice).map(
                                                    sprice, fields_mapping={"order_id": order.id}
                                                ),
                                            )
                                        else:
                                            removed_security_prices.remove(security_price.id)
                                            if not sprice._is_identical_to_db_entity(entity=security_price):
                                                existing_security_prices.append(
                                                    mapper.to(SecurityPrice).map(
                                                        sprice,
                                                        fields_mapping={
                                                            "id": security_price.id,
                                                            "order_id": order.id,
                                                        },
                                                    ),
                                                )

                info_message: str = ""
                if len(removed_security_prices) > 0:
                    delete_result = security_price_collection.delete_many({"_id": {"$in": removed_security_prices}})
                    if delete_result is not None:
                        info_message = f"The {delete_result.deleted_count} security prices data from "
                        info_message += f"{len(removed_security_prices)} has deleted from database."
                        self.__logger.info(info_message)

                if len(removed_orders) > 0:
                    delete_result = order_collection.delete_many({"_id": {"$in": removed_orders}})
                    if delete_result is not None:
                        info_message = f"The {delete_result.deleted_count} orders data from "
                        info_message += f"{len(removed_orders)} has deleted from database."
                        self.__logger.info(info_message)

                if len(new_orders) > 0:
                    docs_dict = []
                    for doc in new_orders:
                        docs_dict.append(doc.dict(by_alias=True))
                    document_ids = order_collection.insert_many(docs_dict).inserted_ids
                    insert_result = self.__convert_many_orders(
                        items=order_collection.find({"_id": {"$in": document_ids}})
                    )
                    if insert_result is not None:
                        info_message = f"The {len(insert_result)} orders data from "
                        info_message += f"{len(new_orders)} has added to database."
                        self.__logger.info(info_message)

                if len(new_security_prices) > 0:
                    orders = self.__convert_many_orders(items=order_collection.find())
                    docs_dict = []
                    for new_security_price in new_security_prices:
                        order = next(
                            (x for x in orders if x.label == new_security_price[0].label),
                            None,
                        )
                        if order is not None:
                            new_security_price[1].order_id = order.id
                        docs_dict.append(new_security_price[1].dict(by_alias=True))
                    document_ids = security_price_collection.insert_many(docs_dict).inserted_ids
                    insert_result = self._convert_many(
                        items=security_price_collection.find({"_id": {"$in": document_ids}})
                    )
                    if insert_result is not None:
                        info_message = f"The {len(insert_result)} security prices data from "
                        info_message += f"{len(new_security_prices)} has added to database."
                        self.__logger.info(info_message)

                if len(missed_security_prices) > 0:
                    docs_dict = []
                    for doc in missed_security_prices:
                        docs_dict.append(doc.dict(by_alias=True))
                    document_ids = security_price_collection.insert_many(docs_dict).inserted_ids
                    insert_result = self._convert_many(
                        items=security_price_collection.find({"_id": {"$in": document_ids}})
                    )
                    if insert_result is not None:
                        info_message = f"The missed {len(insert_result)} security prices data from "
                        info_message += f"{len(missed_security_prices)} has added to database."
                        self.__logger.info(info_message)

                if len(existing_orders) > 0:
                    update_result = 0
                    for existing_order in existing_orders:
                        order_collection.update_one(
                            {"_id": existing_order.id}, {"$set": existing_order.dict(by_alias=True)}
                        )
                        update_result += 1
                    info_message = f"The {update_result} orders data from "
                    info_message += f"{len(existing_orders)} has updated in database."
                    self.__logger.info(info_message)

                if len(existing_security_prices) > 0:
                    update_result = 0
                    for existing_security_price in existing_security_prices:
                        security_price_collection.update_one(
                            {"_id": existing_security_price.id},
                            {"$set": existing_security_price.dict(by_alias=True)},
                        )
                        update_result += 1
                    info_message = f"The {update_result} security prices data from "
                    info_message += f"{len(existing_security_prices)} has updated in database."
                    self.__logger.info(info_message)

        return None
