from pydantic import Field

from app.data_transfer_objects.dto_company import DtoCompany
from app.data_transfer_objects.dto_entity import DtoEntity
from app.data_transfer_objects.dto_financials import DtoFinancials


class DtoCompanyInfo(DtoEntity):
    company: DtoCompany = Field(default_factory=None)
    financial: DtoFinancials = Field(default_factory=[])
