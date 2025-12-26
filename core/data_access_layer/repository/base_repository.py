from contextlib import AbstractContextManager
from typing import Callable, Iterator, List, Optional

from automapper import mapper
from pydantic import BaseModel
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import TextClause

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.entity import DbEntity


class BaseRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        db_model: DbEntity,
    ):
        self.__session_factory = session_factory
        self.__db_model = db_model

    def _convert_to_db_model(self, entity: BaseModel):
        return mapper.map(entity) if entity is not None else None

    def _convert_from_db_model(self, db_entity: DbEntity):
        return mapper.map(db_entity) if db_entity is not None else None

    def _convert_many_to_db_model(self, entities: List[BaseModel]):
        result = []
        for entity in entities:
            result.append(self._convert_to_db_model(entity=entity))
        return result

    def _convert_many_from_db_model(self, db_entities: List[DbEntity]):
        result = []
        for db_entity in db_entities:
            result.append(self._convert_from_db_model(db_entity=db_entity))
        return result

    def _convert_to_dto_model(self, row: Row, model: DtoEntity) -> Optional[DtoEntity]:
        return model.model_validate(dict(row._mapping)) if row is not None else None

    def _convert_many_to_dto_model(self, rows: List[Row], model: DtoEntity) -> List[Optional[DtoEntity]]:
        result: List[Optional[DtoEntity]] = []
        for row in rows:
            result.append(self._convert_to_dto_model(row, model))
        return result

    def session_factory(self):
        return self.__session_factory()

    def get_all(self) -> Iterator[BaseModel]:
        with self.__session_factory() as session:
            return self._convert_many_from_db_model(db_entities=session.query(self.__db_model).all())

    def get_by_id(self, id: int) -> BaseModel:
        with self.__session_factory() as session:
            db_item: Optional[DbEntity] = (
                session.query(self.__db_model).filter(self.__db_model.id == id).first()
                if hasattr(self.__db_model, "id")
                else session.query(self.__db_model).first()
            )
            return (
                self._convert_from_db_model(db_entity=db_item)
                if db_item is not None and hasattr(db_item, "id")
                else None
            )

    def create(self, item: BaseModel) -> None:
        with self.__session_factory() as session:
            if item is not None:
                session.add(self._convert_to_db_model(entity=item))
            return None

    def bulk_save(self, items: List[BaseModel]) -> None:
        with self.__session_factory() as session:
            if len(items) > 0:
                db_items = self._convert_many_to_db_model(entities=items)
                insert_db_items = list(x.__dict__ for x in db_items if not hasattr(x, "id") or x.id is None)
                if len(insert_db_items) > 0:
                    session.bulk_insert_mappings(self.__db_model, insert_db_items)
                update_db_items = list(x.__dict__ for x in db_items if hasattr(x, "id") and x.id is not None)
                if len(update_db_items) > 0:
                    session.bulk_update_mappings(self.__db_model, update_db_items)
            return None

    def _base_fetch_first(
        self, model: DtoEntity, script: TextClause, params: Optional[dict] = None
    ) -> Optional[DtoEntity]:
        result: Optional[DtoEntity] = None
        with self.__session_factory() as session:
            row: Row = session.execute(script).first() if params is None else session.execute(script, params).first()
            if row is not None:
                result = self._convert_to_dto_model(row, model)
        return result

    def _base_fetch_all(
        self, model: DtoEntity, script: TextClause, params: Optional[dict] = None
    ) -> List[Optional[DtoEntity]]:
        result: List[Optional[DtoEntity]] = []
        with self.__session_factory() as session:
            rows: List[Row] = (
                session.execute(script).fetchall() if params is None else session.execute(script, params).fetchall()
            )
            if rows is not None and len(rows) > 0:
                result = self._convert_many_to_dto_model(rows, model)
        return result
