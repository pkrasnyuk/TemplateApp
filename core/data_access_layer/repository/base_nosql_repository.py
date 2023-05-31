from typing import Any, List

from bson.objectid import ObjectId
from pymongo import MongoClient

from core.domain.mongo_entity import MongoEntity


class BaseNoSqlRepository:
    def __init__(self, mongo_client: MongoClient, db_name: str, collection_name: str):
        db = mongo_client[db_name]

        # Create database if it doesn't exist
        if db_name not in mongo_client.list_database_names():
            db.command({"customAction": "CreateDatabase", "offerThroughput": 400})

        # Create collection if it doesn't exist
        if collection_name not in db.list_collection_names():
            db.command({"customAction": "CreateCollection", "collection": collection_name})

        self.collection = db[collection_name]
        self.entity = MongoEntity

    def __convert(self, item: Any):
        return self.entity(**item) if item is not None else None

    def __convert_many(self, items: Any):
        result = []
        for item in items:
            result.append(self.__convert(item))
        return result

    def _get_collection(self):
        return self.__convert_many(self.collection.find())

    def _insert_document(self, doc: MongoEntity):
        document_id = self.collection.insert_one(doc.dict(by_alias=True)).inserted_id
        doc = self.collection.find_one({"_id": document_id})
        return self.__convert(doc)

    def _insert_documents(self, docs: List[MongoEntity]):
        docs_dict = []
        for doc in docs:
            docs_dict.append(doc.dict(by_alias=True))
        document_ids = self.collection.insert_many(docs_dict).inserted_ids
        return self._read_documents({"_id": {"$in": document_ids}})

    def _read_document_by_id(self, id: str):
        doc = self.collection.find_one({"_id": ObjectId(id)})
        return self.__convert(doc)

    def _read_documents(self, condition):
        return self.__convert_many(self.collection.find(condition))

    def _update_document(self, doc: MongoEntity):
        self.collection.update_one({"_id": ObjectId(doc.id)}, {"$set": doc.dict(by_alias=True)})
        return self._read_document_by_id(doc.id)

    def _delete_document(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})
