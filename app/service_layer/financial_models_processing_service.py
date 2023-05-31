import random
from typing import List

from app.data_transfer_objects.dto_company import DtoCompany
from app.data_transfer_objects.dto_company_info import DtoCompanyInfo
from app.data_transfer_objects.dto_derived_financials import DtoDerivedFinancials
from app.data_transfer_objects.dto_financials import DtoFinancials
from app.service_layer.processing_service import ProcessingService
from core.domain.enums import FinancialsType
from core.helpers.common import generate_datetime


class FinancialModelsProcessingService(ProcessingService):
    def processing(self) -> List[DtoCompanyInfo]:
        processing_data: List[DtoCompanyInfo] = []

        for i in range(300):
            company: DtoCompany = DtoCompany(name=f"company_{i}", analyst=f"analyst_{random.randint(0, i)}")
            financials: List[DtoFinancials] = []
            for j in range(random.randint(10, 40)):
                financials.append(
                    DtoFinancials(
                        type=FinancialsType.ANNUAL if j % 2 == 0 else FinancialsType.QUARTERLY,
                        dt=generate_datetime(year=2023, month=random.randint(1, 12), day=random.randint(1, 25)),
                        label=f"financial_{j}",
                        price=10.0 * j * random.random(),
                        dto_derived_financials=DtoDerivedFinancials(
                            total_profit=j * random.random(), total_price=100.0 * j * random.random()
                        ),
                    )
                )
            processing_data.append(DtoCompanyInfo(company=company, financials=financials))

        return processing_data
