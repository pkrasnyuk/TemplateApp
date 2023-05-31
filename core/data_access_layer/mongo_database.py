from contextlib import AbstractContextManager, contextmanager
from typing import Callable

import pymongo


class MongoDatabase:
    def __init__(self, connection_string: str) -> None:
        self.__client = pymongo.MongoClient(connection_string)
        try:
            self.__client.server_info()  # validate connection string
        except pymongo.errors.ServerSelectionTimeoutError:
            raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    @contextmanager  # type: ignore
    def client(self) -> Callable[..., AbstractContextManager[pymongo.MongoClient]]:
        return self.__client
