from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import Field, model_validator

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.enums import RequestStatus


class DtoPricing(DtoEntity):
    status: RequestStatus = Field(default=RequestStatus.PRICE)
    request_id: UUID = Field(default=uuid4)
    dt: date = Field(alias="date", default=datetime.now().date())
    level: float
    pricing: float = Field(ge=0.0, le=100.0, default=0.0)

    @model_validator(mode="before")
    @classmethod
    def check_values(cls, values):
        if "date" not in values or values["date"] is None:
            raise ValueError("a date value must be specified")
        try:
            date.fromisoformat(values["date"])
        except ValueError:
            raise ValueError("incorrect date format for date field, should be YYYY-MM-dd")

        if "level" not in values or values["level"] is None:
            raise ValueError("a level value must be specified")

        if "pricing" not in values or values["pricing"] is None:
            raise ValueError("a pricing value must be specified")

        return values
