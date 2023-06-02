import logging
import time
from typing import List

from app.data_access_layer.repository.security_price_repository import SecurityPriceRepository
from app.data_transfer_objects.dto_security_price import DtoSecurityPrice
from app.service_layer.data_processing_service import DataProcessingService
from core.helpers.common import value2str


class SecurityPriceDataProcessingService(DataProcessingService):
    def __init__(
        self,
        security_price_repository: SecurityPriceRepository,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__security_price_repository = security_price_repository

    def processing(self, data: List[DtoSecurityPrice]) -> List[str]:
        start = time.time()
        self.__security_price_repository.bulk_save(items=data)
        end = time.time()
        elapsed_time = end - start
        self.__logger.info(f"Execution time for save data: {elapsed_time} seconds")
        return self.__generate_operation_results(data=data)

    def __generate_operation_results(self, data: List[DtoSecurityPrice]) -> List[str]:
        operation_results: List[str] = []
        result_message: str = ""
        for item in data:
            result_message = f"Security price model updated for {value2str(item.ticker, string_length=256)}, "
            result_message += f"{value2str(value=item.date)}, {value2str(value=item.price)}."
            operation_results.append(result_message)

        return operation_results
