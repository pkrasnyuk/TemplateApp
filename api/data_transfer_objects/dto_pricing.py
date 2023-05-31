from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import Field, root_validator

from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.enums import RequestStatus


class DtoPricing(DtoEntity):
    status: RequestStatus = Field(default_factory=RequestStatus.PRICE)
    request_id: UUID = Field(default_factory=uuid4)
    dt: date = Field(alias="date", default_factory=datetime.now().date())
    level: float
    pricing: float = Field(ge=0.0, le=100.0, default=0.0)

    @root_validator(pre=True)
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
