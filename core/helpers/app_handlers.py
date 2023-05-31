import logging
import sys
import traceback

from core.service_layer.slack_notification_service import SlackNotificationService


class AppHandlers:
    def __init__(
        self,
        notification_service: SlackNotificationService,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__notification_service = notification_service

    def __exception_handler(self, exctype, value, tb):
        self.__logger.error(msg=f"An unhandled exception of type {exctype}: ", exc_info=value, stack_info=True)
        self.__notification_service.send_error_message(
            message="A critical error interrupted import process.",
            ex=value,
            traceback="".join(traceback.extract_tb(tb).format()),
        )

    def init_global_handler(self):
        sys.excepthook = self.__exception_handler
