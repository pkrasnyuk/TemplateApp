from datetime import datetime
from typing import List
from uuid import UUID

import pytz
from automapper import mapper

from api.data_access_layer.repository.pricing_repository import PricingRepository
from api.data_transfer_objects.dto_pricing import DtoPricing
from core.domain.pricing import Pricing
from core.helpers.common import date2datetime


class PricingService:
    def __init__(self, repository: PricingRepository):
        self.__repository = repository

    def request_processing(self, entities: List[DtoPricing], user_id: int) -> None:
        not_unique_request_ids: List[UUID] = []
        pricings: List[Pricing] = []
        if entities is not None and len(entities) > 0:
            ts_value: datetime = pytz.utc.localize(datetime.now())
            for entity in entities:
                if self.__repository.get_pricing(request_id=entity.request_id, user_id=user_id) is not None:
                    not_unique_request_ids.append(entity.request_id)
                else:
                    pricings.append(
                        mapper.to(Pricing).map(
                            entity,
                            fields_mapping={
                                "ts": ts_value,
                                "user_id": user_id,
                                "user_request_id": entity.request_id,
                                "date": date2datetime(entity.dt),
                            },
                        )
                    )
        if len(not_unique_request_ids) > 0:
            ids = ", ".join([str(x) for x in not_unique_request_ids])
            raise Exception(f"The pricing request ids=[{ids}] are not unique (used in previous requests).")
        else:
            return self.__repository.bulk_save(entities=pricings)
