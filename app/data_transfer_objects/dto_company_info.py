from typing import List

from pydantic import Field

from app.data_transfer_objects.dto_company import DtoCompany
from app.data_transfer_objects.dto_financials import DtoFinancials
from core.data_transfer_objects.dto_entity import DtoEntity


class DtoCompanyInfo(DtoEntity):
    company: DtoCompany = Field(default_factory=None)
    financials: List[DtoFinancials] = Field(default_factory=[])
