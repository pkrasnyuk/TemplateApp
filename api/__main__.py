from api.application import Application
from api.containers import Container
from core.helpers.app_handlers import AppHandlers


def main(handlers: AppHandlers, application: Application) -> None:
    handlers.init_global_handler()
    application.start()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    application = Application(container=container)

    main(handlers=container.handlers(), application=application)
