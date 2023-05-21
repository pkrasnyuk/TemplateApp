from signal import SIGINT, signal

from app.containers import Container
from app.helpers.app_handlers import AppHandlers
from app.service_layer.data_processing_service import DataProcessingService


def main(handlers: AppHandlers, service: DataProcessingService) -> None:
    signal(SIGINT, __handler)

    handlers.init_global_handler()

    service.processing()

    print("The template app is working. \r\n" "Press CTRL+C to quit.")
    while True:
        pass


def __handler(signal_received, frame) -> None:
    print("done.")
    exit(0)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(handlers=container.handlers(), service=container.financial_processing_service())
