import logging
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from pymongo import MongoClient, errors


class MongoDatabase:
    def __init__(self, connection_string: str) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__client = MongoClient(connection_string)
        try:
            self.__client.server_info()
        except errors.ServerSelectionTimeoutError:
            raise TimeoutError("MongoDB server not available")

    @contextmanager  # type: ignore
    def client(self) -> Callable[..., AbstractContextManager[MongoClient]]:  # type: ignore
        client: MongoClient = self.__client
        try:
            yield client
        except Exception:
            self.__logger.exception("MongoDB client throw exception")
            raise
