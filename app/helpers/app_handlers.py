import logging
import sys


class AppHandlers:
    def __init__(
        self,
    ):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def __exception_handler(self, exctype, value, tb):
        self.__logger.error(msg=f"An unhandled exception of type {exctype}: ", exc_info=value, stack_info=True)

    def init_global_handler(self):
        sys.excepthook = self.__exception_handler
