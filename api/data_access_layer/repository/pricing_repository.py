from contextlib import AbstractContextManager
from typing import Callable, List, Optional
from uuid import UUID

from automapper import mapper
from sqlalchemy.orm import Session

from core.data_access_layer.repository.base_repository import BaseRepository
from core.domain.pricing import DbPricing, Pricing
from core.helpers.common import date2datetime, min_datetime


class PricingRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory=session_factory, db_model=DbPricing)  # type: ignore

    def _convert_to_db_model(self, entity: Pricing):
        return (
            mapper.to(DbPricing).map(
                entity, fields_mapping={"status": entity.status.value, "user_request_id": str(entity.user_request_id)}
            )
            if entity is not None
            else None
        )

    def bulk_save(self, entities: List[Pricing]) -> None:
        super().bulk_save(entities)

    def get_pricing(self, request_id: UUID, user_id: int) -> Optional[Pricing]:
        with self.session_factory() as session:
            db_pricing: DbPricing = (
                session.query(DbPricing)
                .filter(
                    DbPricing.user_request_id == str(request_id),
                    DbPricing.user_id == user_id,
                )
                .first()
            )
            return (
                mapper.to(Pricing).map(
                    db_pricing,
                    fields_mapping={
                        "date": date2datetime(dt=db_pricing.date)
                        if db_pricing.date is not None
                        else min_datetime().date()
                    },
                )
                if db_pricing is not None
                else None
            )
