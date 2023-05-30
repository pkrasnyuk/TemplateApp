import logging
import traceback
from typing import Callable, List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.service_layer.scheduler_job_wrapper import SchedulerJobWrapper
from app.service_layer.slack_notification_service import SlackNotificationService


class SchedulerService:
    def __init__(
        self,
        scheduler_job_wrappers: List[SchedulerJobWrapper],
        notification_service: SlackNotificationService,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__scheduler: BackgroundScheduler = BackgroundScheduler(daemon=True, logger=self.__logger)
        self.__scheduler_name: str = "app background scheduler"
        self.__scheduler_job_wrappers: List[SchedulerJobWrapper] = scheduler_job_wrappers
        self.__notification_service = notification_service

    def run(self) -> None:
        try:
            if self.__scheduler_job_wrappers is not None and len(self.__scheduler_job_wrappers) > 0:
                for scheduler_job_wrapper in self.__scheduler_job_wrappers:
                    job_info = scheduler_job_wrapper.get_job_info()
                    self.__scheduler.add_job(
                        self.__catch_exception(
                            job_method=scheduler_job_wrapper.execute_scheduler_job, job_name=job_info.name
                        ),
                        CronTrigger.from_crontab(expr=job_info.crontab, timezone="UTC"),
                        name=job_info.name,
                    )
            self.__scheduler.start()
            self.__logger.info(f"The {self.__scheduler_name} has been successfully started.")
        except (KeyboardInterrupt, SystemExit) as ex:
            self.__logger.error(msg="failed to execute service", exc_info=ex, stack_info=True)
            self.stop()

    def stop(self) -> None:
        if self.__scheduler and self.__scheduler.running:
            self.__scheduler.shutdown()
            self.__logger.info(f"The {self.__scheduler_name} has shutdown.")

    def __catch_exception(self, job_method: Callable[[], None], job_name: str):
        def wrapper():
            try:
                job_method()
            except Exception as ex:
                self.__logger.error(msg=f"failed to execute job {job_name}", exc_info=ex, stack_info=True)
                self.__notification_service.send_error_message(
                    message="A critical error interrupted import process.",
                    ex=ex,
                    traceback=traceback.format_exc(),
                )

        return wrapper
