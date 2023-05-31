import logging
from typing import List

from app.service_layer.data_processing_service import DataProcessingService
from app.service_layer.processing_service import ProcessingService
from core.data_transfer_objects.dto_entity import DtoEntity
from core.domain.scheduler_job import SchedulerJob
from core.service_layer.slack_notification_service import SlackNotificationService


class SchedulerJobWrapper:
    def __init__(
        self,
        job: SchedulerJob,
        processing_service: ProcessingService,
        data_processing_service: DataProcessingService,
        notification_service: SlackNotificationService,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__job = job
        self.__processing_service = processing_service
        self.__data_processing_service = data_processing_service
        self.__notification_service = notification_service

    def get_job_info(self) -> SchedulerJob:
        return self.__job

    def execute_scheduler_job(self) -> None:
        self.__logger.info(f"The job {self.__job.name} is starting...")
        info_data: List[DtoEntity] = self.__processing_service.processing()
        result_data: List[str] = self.__data_processing_service.processing(data=info_data)
        self.__notification_service.send_notification_messages(messages=result_data)
