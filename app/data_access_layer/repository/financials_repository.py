from contextlib import AbstractContextManager
from datetime import date, datetime
from typing import Callable, List, Optional

from automapper import mapper
from sqlalchemy.orm import Session

from app.data_access_layer.repository.base_repository import BaseRepository
from app.data_transfer_objects.dto_company_info import DtoCompanyInfo
from app.domain.company import DbCompany
from app.domain.derived_financials import DbDerivedFinancials
from app.domain.financials import DbFinancials, Financials
from app.helpers.common import date2datetime


class FinancialsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory=session_factory, db_model=DbFinancials)  # type: ignore

    def _conver_from_db_model(self, db_entity: DbFinancials):
        return (
            mapper.to(Financials).map(db_entity, fields_mapping={"dt": date2datetime(db_entity.dt)})
            if db_entity is not None and db_entity.dt is not None and isinstance(db_entity.dt, (date, datetime))
            else None
        )

    def bulk_save(self, items: List[DtoCompanyInfo]) -> None:
        with self.session_factory() as session:
            last_updated: datetime = datetime.utcnow()
            db_companies: List[DbCompany] = session.query(DbCompany).order_by(DbCompany.name).all()
            for item in items:
                if item and item.company and item.company.name:
                    db_company: Optional[DbCompany] = next(
                        (x for x in db_companies if x.name and x.name.lower() == item.company.name.lower()), None
                    )
                    if db_company is None:
                        new_financials: List[DbFinancials] = []
                        if item.financials is not None and len(item.financials) > 0:
                            for fitem in item.financials:
                                if fitem is not None:
                                    financials: DbFinancials = mapper.to(DbFinancials).map(
                                        fitem,
                                        fields_mapping={
                                            "id": None,
                                            "company_id": None,
                                            "last_updated": last_updated,
                                        },
                                    )
                                    if fitem.dto_derived_financials is not None:
                                        financials.derived_financials = mapper.to(DbDerivedFinancials).map(
                                            fitem.dto_derived_financials,
                                            fields_mapping={"id": None},
                                        )
                                    new_financials.append(financials)
                        new_company: DbCompany = DbCompany(
                            name=item.company.name, analyst=item.company.analyst, financials=new_financials
                        )
                        session.add(new_company)

        return None
