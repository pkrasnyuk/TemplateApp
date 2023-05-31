import logging

import uvicorn
from fastapi import FastAPI

from api.containers import Container

from . import endpoints, users_endpoints


class Application:
    def __init__(self, container: Container):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.api = FastAPI(
            title="App Api",
            redoc_url=None,
            docs_url="/docs",
        )
        self.api.container = container
        self.api.include_router(endpoints.router)
        self.api.include_router(users_endpoints.router)

    def start(self):
        try:
            if self.api:
                uvicorn.run(
                    self.api,
                    port=int(self.api.container.config.api.port()),
                    host=self.api.container.config.api.host(),
                    timeout_keep_alive=0,
                    log_config=self.api.container.config.log(),
                )
        except (KeyboardInterrupt, SystemExit) as ex:
            self.__logger.error(msg="failed to execute application", exc_info=ex, stack_info=True)
