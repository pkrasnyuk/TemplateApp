from contextlib import AbstractContextManager
from datetime import date, datetime
from typing import Callable

from automapper import mapper
from sqlalchemy.orm import Session

from app.data_access_layer.repository.base_repository import BaseRepository
from app.domain.financials import DbFinancials, Financials
from app.helpers.common import date2datetime


class FinancialsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory=session_factory, db_model=DbFinancials)  # type: ignore

    def _conver_from_db_model(self, db_entity: DbFinancials):
        return (
            mapper.to(Financials).map(db_entity, fields_mapping={"dt": date2datetime(db_entity.dt)})
            if db_entity is not None and db_entity.dt is not None and isinstance(db_entity.dt, (date, datetime))
            else None
        )
