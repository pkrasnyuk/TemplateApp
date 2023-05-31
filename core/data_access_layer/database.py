import logging
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session


class Database:
    def __init__(self, connection_string: str) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__engine = create_engine(
            "mssql+pyodbc:///?odbc_connect=%s" % connection_string,
            fast_executemany=True,
        )
        self.__session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.__engine,
            ),
        )

    @contextmanager  # type: ignore
    def session(self) -> Callable[..., AbstractContextManager[Session]]:  # type: ignore
        session: Session = self.__session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            self.__logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
