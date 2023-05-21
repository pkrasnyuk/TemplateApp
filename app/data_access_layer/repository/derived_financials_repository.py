from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.data_access_layer.repository.base_repository import BaseRepository
from app.domain.derived_financials import DbDerivedFinancials


class DerivedFinancialsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory=session_factory, db_model=DbDerivedFinancials)  # type: ignore
