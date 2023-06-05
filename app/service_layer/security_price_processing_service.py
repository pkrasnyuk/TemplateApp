import random
from typing import List, Optional

from app.data_transfer_objects.dto_order import DtoOrder
from app.data_transfer_objects.dto_order_info import DtoOrderInfo
from app.data_transfer_objects.dto_security_price import DtoSecurityPrice
from app.service_layer.processing_service import ProcessingService
from core.helpers.common import generate_datetime


class SecurityPriceProcessingService(ProcessingService):
    def processing(self) -> List[DtoOrderInfo]:
        processing_data: List[DtoOrderInfo] = []

        for i in range(300):
            order: DtoOrder = DtoOrder(
                label=f"label_{i}",
                date=generate_datetime(year=2023, month=random.randint(1, 12), day=random.randint(1, 28)),
            )
            security_prices: List[DtoSecurityPrice] = []
            for j in range(random.randint(10, 40)):
                security_price_name: str = f"security_price_{random.randint(0, j)}"
                existing_security_price: Optional[DtoSecurityPrice] = next(
                    (x for x in security_prices if x.ticker == security_price_name),
                    None,
                )
                if existing_security_price is None:
                    security_prices.append(
                        DtoSecurityPrice(
                            ticker=security_price_name,
                            price=10.0 * j * random.random(),
                        )
                    )
            processing_data.append(DtoOrderInfo(order=order, security_prices=security_prices))
        return processing_data
