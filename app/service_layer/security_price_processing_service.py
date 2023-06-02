import random
from typing import List

from app.data_transfer_objects.dto_security_price import DtoSecurityPrice
from app.service_layer.processing_service import ProcessingService
from core.helpers.common import generate_datetime


class SecurityPriceProcessingService(ProcessingService):
    def processing(self) -> List[DtoSecurityPrice]:
        processing_data: List[DtoSecurityPrice] = []

        for i in range(300):
            processing_data.append(
                DtoSecurityPrice(
                    date=generate_datetime(year=2023, month=random.randint(1, 12), day=random.randint(1, 28)),
                    ticker=f"security_price_{random.randint(1, 10)}",
                    price=10.0 * i * random.random(),
                )
            )

        return processing_data
