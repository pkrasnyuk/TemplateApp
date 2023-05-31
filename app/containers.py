import logging.config
import os

from automapper import mapper
from dependency_injector import containers, providers

from app.data_access_layer.repository.company_repository import CompanyRepository
from app.data_access_layer.repository.derived_financials_repository import DerivedFinancialsRepository
from app.data_access_layer.repository.financials_repository import FinancialsRepository
from app.data_access_layer.repository.security_price_repository import SecurityPriceRepository
from app.data_transfer_objects.dto_company import DtoCompany
from app.data_transfer_objects.dto_derived_financials import DtoDerivedFinancials
from app.data_transfer_objects.dto_financials import DtoFinancials
from app.service_layer.financial_models_data_processing_service import FinancialModelsDataProcessingService
from app.service_layer.financial_models_processing_service import FinancialModelsProcessingService
from app.service_layer.scheduler_job_wrapper import SchedulerJobWrapper
from app.service_layer.scheduler_service import SchedulerService
from core.data_access_layer.database import Database
from core.data_access_layer.mongo_database import MongoDatabase
from core.domain.company import Company, DbCompany
from core.domain.derived_financials import DbDerivedFinancials, DerivedFinancials
from core.domain.financials import DbFinancials, Financials
from core.domain.scheduler_job import SchedulerJob
from core.helpers.app_handlers import AppHandlers
from core.service_layer.slack_notification_service import SlackNotificationService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_yaml(filepath=os.path.dirname(__file__) + "/config.yaml", required=True)

    slack_config = config.slack()
    mongo_config = config.mongo()

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    db = providers.Singleton(Database, connection_string=config.db_connection_string())
    db_mongo = providers.Singleton(MongoDatabase, connection_string=mongo_config["connection_string"])

    mapper.add(DbCompany, Company)
    mapper.add(Company, DbCompany)
    mapper.add(DtoCompany, DbCompany)
    mapper.add(DbFinancials, Financials)
    mapper.add(Financials, DbFinancials)
    mapper.add(DtoFinancials, DbFinancials)
    mapper.add(DbDerivedFinancials, DerivedFinancials)
    mapper.add(DerivedFinancials, DbDerivedFinancials)
    mapper.add(DtoDerivedFinancials, DbDerivedFinancials)

    company_repository = providers.Factory(CompanyRepository, session_factory=db.provided.session)
    financials_repository = providers.Factory(FinancialsRepository, session_factory=db.provided.session)
    derived_financials_repository = providers.Factory(DerivedFinancialsRepository, session_factory=db.provided.session)

    security_price_repository = providers.Factory(
        SecurityPriceRepository, mongo_client=db_mongo.provided.client, db_name=mongo_config["database"]
    )

    slack_notification_service = providers.Singleton(
        SlackNotificationService,
        webhook_url=slack_config["webhook_url"],
        token=slack_config["token"],
        channel=slack_config["channel"],
    )

    handlers = providers.Singleton(
        AppHandlers,
        notification_service=slack_notification_service,
    )

    scheduler_job_wrapper_providers_list = providers.List()
    financial_models_job_config = config.financial_models_job()

    financial_models_processing_service = providers.Factory(
        FinancialModelsProcessingService,
    )
    financial_models_data_processing_service = providers.Factory(
        FinancialModelsDataProcessingService,
        financials_repository=financials_repository,
    )
    scheduler_job_wrapper_providers_list.add_args(
        providers.Factory(
            SchedulerJobWrapper,
            job=SchedulerJob(name=financial_models_job_config["name"], crontab=financial_models_job_config["crontab"]),
            processing_service=financial_models_processing_service,
            data_processing_service=financial_models_data_processing_service,
            notification_service=slack_notification_service,
        )
    )

    scheduler_service = providers.Factory(
        SchedulerService,
        scheduler_job_wrappers=scheduler_job_wrapper_providers_list,
        notification_service=slack_notification_service,
    )
