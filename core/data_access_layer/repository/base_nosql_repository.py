from contextlib import AbstractContextManager, contextmanager
from typing import Any, Callable, List, Optional

from bson.objectid import ObjectId
from pymongo import MongoClient

from core.domain.mongo_entity import MongoEntity


class BaseNoSqlRepository:
    def __init__(
        self, mongo_client: Callable[..., AbstractContextManager[MongoClient]], db_name: str, collection_name: str
    ):
        self.__client = contextmanager(mongo_client)  # type: ignore
        with self.__client() as db_client:
            db = db_client[db_name]

            # # Need for Azure Cosmos DB for MongoDB
            # # Create database if it doesn't exist
            # if db_name not in db_client.list_database_names():
            #     db.command({"customAction": "CreateDatabase", "offerThroughput": 400})

            # # Create collection if it doesn't exist
            # if collection_name not in db.list_collection_names():
            #     db.command({"customAction": "CreateCollection", "collection": collection_name})

            self.collection = db[collection_name]
            self.entity = MongoEntity

    def __convert(self, item: Any) -> Optional[MongoEntity]:
        return self.entity(**item) if item is not None else None

    def __convert_many(self, items: Any) -> List[MongoEntity]:
        result: List[MongoEntity] = []
        for item in items:
            entity: Optional[MongoEntity] = self.__convert(item)
            if entity is not None:
                result.append(entity)
        return result

    def _get_collection(self) -> List[MongoEntity]:
        return self.__convert_many(self.collection.find())

    def _insert_document(self, doc: MongoEntity) -> Optional[MongoEntity]:
        document_id = self.collection.insert_one(doc.dict(by_alias=True)).inserted_id
        doc = self.collection.find_one({"_id": document_id})
        return self.__convert(doc)

    def _insert_documents(self, docs: List[MongoEntity]) -> List[MongoEntity]:
        docs_dict = []
        for doc in docs:
            docs_dict.append(doc.dict(by_alias=True))
        document_ids = self.collection.insert_many(docs_dict).inserted_ids
        return self._read_documents({"_id": {"$in": document_ids}})

    def _read_document_by_id(self, id: str) -> Optional[MongoEntity]:
        doc = self.collection.find_one({"_id": ObjectId(id)})
        return self.__convert(doc)

    def _read_documents(self, condition) -> List[MongoEntity]:
        return self.__convert_many(self.collection.find(condition))

    def _update_document(self, doc: MongoEntity) -> Optional[MongoEntity]:
        self.collection.update_one({"_id": ObjectId(doc.id)}, {"$set": doc.dict(by_alias=True)})
        return self._read_document_by_id(doc.id)

    def _delete_document(self, id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(id)})
