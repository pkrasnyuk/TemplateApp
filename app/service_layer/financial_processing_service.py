import logging

from app.data_access_layer.repository.financials_repository import FinancialsRepository
from app.service_layer.data_processing_service import DataProcessingService


class FinancialProcessingService(DataProcessingService):
    def __init__(
        self,
        financials_repository: FinancialsRepository,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__financials_repository = financials_repository

    def processing(self) -> None:
        return None
