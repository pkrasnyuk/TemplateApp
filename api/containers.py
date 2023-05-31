import logging.config
import os

from automapper import mapper
from dependency_injector import containers, providers

from api.data_access_layer.repository.pricing_repository import PricingRepository
from api.data_access_layer.repository.user_repository import UserRepository
from api.data_transfer_objects.dto_pricing import DtoPricing
from api.data_transfer_objects.dto_user import DtoUser
from api.service_layer.pricing_service import PricingService
from api.service_layer.user_service import UserService
from core.data_access_layer.database import Database
from core.domain.pricing import DbPricing, Pricing
from core.domain.user import DbUser, User
from core.helpers.app_handlers import AppHandlers
from core.service_layer.slack_notification_service import SlackNotificationService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints", ".users_endpoints"])

    config = providers.Configuration()
    config.from_yaml(filepath=os.path.dirname(__file__) + "/config.yaml", required=True)

    slack_config = config.slack()

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    db = providers.Singleton(Database, connection_string=config.db_connection_string())

    mapper.add(DbUser, User)
    mapper.add(User, DbUser)
    mapper.add(DtoUser, DbUser)
    mapper.add(DbPricing, Pricing)
    mapper.add(Pricing, DbPricing)
    mapper.add(DtoPricing, DbPricing)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    pricing_repository = providers.Factory(PricingRepository, session_factory=db.provided.session)

    user_service = providers.Factory(UserService, repository=user_repository)
    pricing_service = providers.Factory(PricingService, repository=pricing_repository)

    slack_notification_service = providers.Singleton(
        SlackNotificationService,
        webhook_url=slack_config["webhook_url"],
        token=slack_config["token"],
        channel=slack_config["channel"],
    )

    handlers = providers.Singleton(AppHandlers, notification_service=slack_notification_service)
