import logging
from typing import List

from app.data_access_layer.repository.financials_repository import FinancialsRepository
from app.data_transfer_objects.dto_company import DtoCompany
from app.data_transfer_objects.dto_company_info import DtoCompanyInfo
from app.data_transfer_objects.dto_derived_financials import DtoDerivedFinancials
from app.data_transfer_objects.dto_financials import DtoFinancials
from app.domain.enums import FinancialsType
from app.helpers.common import generate_datetime
from app.service_layer.data_processing_service import DataProcessingService


class FinancialProcessingService(DataProcessingService):
    def __init__(
        self,
        financials_repository: FinancialsRepository,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__financials_repository = financials_repository

    def processing(self) -> None:
        processing_data: List[DtoCompanyInfo] = []

        company: DtoCompany = DtoCompany(name="company", analyst="analyst")
        financials: List[DtoFinancials] = []
        financials.append(
            DtoFinancials(
                type=FinancialsType.ANNUAL,
                dt=generate_datetime(year=2023, month=1, day=1),
                label="financial_1",
                price=0.0,
                dto_derived_financials=DtoDerivedFinancials(total_profit=0.0, total_price=0.0),
            )
        )
        financials.append(
            DtoFinancials(
                type=FinancialsType.QUARTERLY,
                dt=generate_datetime(year=2023, month=2, day=1),
                label="financial_2",
                price=None,
                dto_derived_financials=DtoDerivedFinancials(total_profit=None, total_price=None),
            )
        )
        financials.append(
            DtoFinancials(
                type=FinancialsType.ANNUAL,
                dt=generate_datetime(year=2023, month=3, day=1),
                label="financial_3",
                price=10.0,
                dto_derived_financials=DtoDerivedFinancials(total_profit=5.0, total_price=10.0),
            )
        )
        processing_data.append(DtoCompanyInfo(company=company, financials=financials))

        return self.__financials_repository.bulk_save(items=processing_data)
