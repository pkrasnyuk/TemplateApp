import logging
import time
from typing import List

from app.data_access_layer.repository.financials_repository import FinancialsRepository
from app.data_transfer_objects.dto_company_info import DtoCompanyInfo
from app.service_layer.data_processing_service import DataProcessingService


class FinancialModelsDataProcessingService(DataProcessingService):
    def __init__(
        self,
        financials_repository: FinancialsRepository,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__financials_repository = financials_repository

    def processing(self, data: List[DtoCompanyInfo]) -> List[str]:
        start = time.time()
        self.__financials_repository.bulk_save(items=data)
        end = time.time()
        elapsed_time = end - start
        self.__logger.info(f"Execution time for save data: {elapsed_time} seconds")
        return self.__generate_operation_results(data=data)

    def __generate_operation_results(self, data: List[DtoCompanyInfo]) -> List[str]:
        operation_results: List[str] = []
        result_message: str = ""
        for item in data:
            for fitem in item.financials:
                result_message = f"Financial model updated for {item.company.name}, "
                result_message += f"{fitem.label} ({item.company.analyst})."
                operation_results.append(result_message)
        return operation_results
