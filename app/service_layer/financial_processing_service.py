import logging
import random
import time
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

        for i in range(300):
            company: DtoCompany = DtoCompany(name=f"company_{i}", analyst=f"analyst_{random.randint(0, i)}")
            financials: List[DtoFinancials] = []
            for j in range(random.randint(10, 40)):
                financials.append(
                    DtoFinancials(
                        type=FinancialsType.ANNUAL,
                        dt=generate_datetime(year=2023, month=random.randint(1, 12), day=random.randint(1, 25)),
                        label=f"financial_{j}",
                        price=10.0 * j * random.random(),
                        dto_derived_financials=DtoDerivedFinancials(
                            total_profit=j * random.random(), total_price=100.0 * j * random.random()
                        ),
                    )
                )
            processing_data.append(DtoCompanyInfo(company=company, financials=financials))

        start = time.time()
        self.__financials_repository.bulk_save(items=processing_data)
        end = time.time()
        elapsed_time = end - start
        self.__logger.info(f"Execution time: {elapsed_time} seconds")

        return None
