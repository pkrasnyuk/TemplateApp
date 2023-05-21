import logging.config
import os

from automapper import mapper
from dependency_injector import containers, providers

from app.data_access_layer.database import Database
from app.data_access_layer.repository.company_repository import CompanyRepository
from app.data_access_layer.repository.derived_financials_repository import DerivedFinancialsRepository
from app.data_access_layer.repository.financials_repository import FinancialsRepository
from app.data_transfer_objects.dto_company import DtoCompany
from app.data_transfer_objects.dto_derived_financials import DtoDerivedFinancials
from app.data_transfer_objects.dto_financials import DtoFinancials
from app.domain.company import Company, DbCompany
from app.domain.derived_financials import DbDerivedFinancials, DerivedFinancials
from app.domain.financials import DbFinancials, Financials
from app.helpers.app_handlers import AppHandlers
from app.service_layer.financial_processing_service import FinancialProcessingService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_yaml(filepath=os.path.dirname(__file__) + "/config.yaml", required=True)

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    handlers = providers.Singleton(AppHandlers)

    db = providers.Singleton(Database, connection_string=config.db_connection_string())

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

    financial_processing_service = providers.Factory(
        FinancialProcessingService,
        financials_repository=financials_repository,
    )
