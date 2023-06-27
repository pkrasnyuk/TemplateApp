import logging
from contextlib import AbstractContextManager
from datetime import date, datetime
from typing import Callable, List, Optional

from automapper import mapper
from sqlalchemy.orm import Session

from app.data_transfer_objects.dto_company_info import DtoCompanyInfo
from core.data_access_layer.repository.base_repository import BaseRepository
from core.domain.company import DbCompany
from core.domain.derived_financials import DbDerivedFinancials
from core.domain.financials import DbFinancials, Financials
from core.helpers.common import date2datetime


class FinancialsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory=session_factory, db_model=DbFinancials)  # type: ignore
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def _convert_from_db_model(self, db_entity: DbFinancials):
        return (
            mapper.to(Financials).map(db_entity, fields_mapping={"dt": date2datetime(db_entity.dt)})
            if db_entity is not None and db_entity.dt is not None and isinstance(db_entity.dt, (date, datetime))
            else None
        )

    def bulk_save(self, items: List[DtoCompanyInfo]) -> None:
        with self.session_factory() as session:
            last_updated: datetime = datetime.utcnow()
            db_companies: List[DbCompany] = session.query(DbCompany).order_by(DbCompany.name).all()
            removed_companies: List[int] = [x.id for x in db_companies]
            for item in items:
                if item is not None and item.company is not None and item.company.name:
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
                    else:
                        removed_companies.remove(db_company.id)
                        if not item.company._is_identical_to_db_entity(entity=db_company):
                            session.bulk_update_mappings(
                                DbCompany,
                                [mapper.to(DbCompany).map(item.company, fields_mapping={"id": db_company.id}).__dict__],
                            )
                        db_company_financials: List[DbFinancials] = (
                            session.query(DbFinancials).filter(DbFinancials.company_id == db_company.id).all()
                        )
                        db_company_financials_ids: List[int] = [x.id for x in db_company_financials]
                        db_company_derived_financials: List[DbDerivedFinancials] = (
                            session.query(DbDerivedFinancials)
                            .filter(DbDerivedFinancials.id.in_(db_company_financials_ids))
                            .all()
                        )
                        new_financials = []
                        existing_financials: List[DbFinancials] = []
                        removed_financials: List[int] = db_company_financials_ids
                        new_derived_financials: List[DbDerivedFinancials] = []
                        existing_derived_financials: List[DbDerivedFinancials] = []
                        if item.financials is not None and len(item.financials) > 0:
                            for fitem in item.financials:
                                if fitem is not None:
                                    db_company_finance: Optional[DbFinancials] = next(
                                        (
                                            x
                                            for x in db_company_financials
                                            if x.type == fitem.type
                                            and x.dt == fitem.dt.date()
                                            and x.label == fitem.label
                                        ),
                                        None,
                                    )
                                    if db_company_finance is None:
                                        financials = mapper.to(DbFinancials).map(
                                            fitem,
                                            fields_mapping={
                                                "id": None,
                                                "company_id": db_company.id,
                                                "last_updated": last_updated,
                                            },
                                        )
                                        if fitem.dto_derived_financials is not None:
                                            financials.derived_financials = mapper.to(DbDerivedFinancials).map(
                                                fitem.dto_derived_financials,
                                                fields_mapping={"id": None},
                                            )
                                        new_financials.append(financials)
                                    else:
                                        removed_financials.remove(db_company_finance.id)
                                        if not fitem._is_identical_to_db_entity(entity=db_company_finance):
                                            existing_financials.append(
                                                mapper.to(DbFinancials).map(
                                                    fitem,
                                                    fields_mapping={
                                                        "id": db_company_finance.id,
                                                        "company_id": db_company.id,
                                                        "last_updated": last_updated,
                                                    },
                                                )
                                            )
                                        if fitem.dto_derived_financials is not None:
                                            db_company_derived_finance: Optional[DbDerivedFinancials] = next(
                                                (
                                                    x
                                                    for x in db_company_derived_financials
                                                    if x.id == db_company_finance.id
                                                ),
                                                None,
                                            )
                                            if db_company_derived_finance is None:
                                                new_derived_financials.append(
                                                    mapper.to(DbDerivedFinancials).map(
                                                        fitem.dto_derived_financials,
                                                        fields_mapping={"id": db_company_finance.id},
                                                    )
                                                )
                                            else:
                                                if not fitem.dto_derived_financials._is_identical_to_db_entity(
                                                    entity=db_company_derived_finance
                                                ):
                                                    existing_derived_financials.append(
                                                        mapper.to(DbDerivedFinancials).map(
                                                            fitem.dto_derived_financials,
                                                            fields_mapping={"id": db_company_finance.id},
                                                        )
                                                    )
                        if len(removed_financials) > 0:
                            delete_result: int = (
                                session.query(DbDerivedFinancials)
                                .filter(DbDerivedFinancials.id.in_(removed_financials))
                                .delete()
                            )
                            info_message: str = (
                                f"The {delete_result} derived financials data from {len(removed_financials)} "
                            )
                            info_message += f"for company '{item.company.name}' has deleted from database."
                            self.__logger.info(info_message)

                            delete_result = (
                                session.query(DbFinancials).filter(DbFinancials.id.in_(removed_financials)).delete()
                            )
                            info_message = f"The {delete_result} financials data from {len(removed_financials)} "
                            info_message += f"for company '{item.company.name}' has deleted from database."
                            self.__logger.info(info_message)
                        if len(new_financials) > 0:
                            existing_db_company: DbCompany = session.query(DbCompany).get(db_company.id)
                            existing_db_company.financials.add_all(new_financials)
                            info_message = f"The {len(new_financials)} financials data for company"
                            info_message += f" '{item.company.name}' has added to database."
                            self.__logger.info(info_message)
                        if len(existing_financials) > 0:
                            session.bulk_update_mappings(
                                DbFinancials,
                                list(x.__dict__ for x in existing_financials),
                            )
                            info_message = f"The {len(existing_financials)} financials data for company"
                            info_message += f" '{item.company.name}' has updated in database."
                            self.__logger.info(info_message)
                        if len(new_derived_financials) > 0:
                            session.bulk_insert_mappings(
                                DbDerivedFinancials,
                                list(x.__dict__ for x in new_derived_financials),
                            )
                            info_message = f"The {len(new_derived_financials)} derived financials data"
                            info_message += f" for company '{item.company.name}' has added to database."
                            self.__logger.info(info_message)
                        if len(existing_derived_financials) > 0:
                            session.bulk_update_mappings(
                                DbDerivedFinancials,
                                list(x.__dict__ for x in existing_derived_financials),
                            )
                            info_message = f"The {len(existing_derived_financials)} derived financials data"
                            info_message += f" for company '{item.company.name}' has updated in database."
                            self.__logger.info(info_message)

            if len(removed_companies) > 0:
                db_company_financials = (
                    session.query(DbFinancials).filter(DbFinancials.company_id.in_(removed_companies)).all()
                )
                if len(db_company_financials) > 0:
                    db_company_financials_ids = [x.id for x in db_company_financials]

                    delete_result = (
                        session.query(DbDerivedFinancials)
                        .filter(DbDerivedFinancials.id.in_(db_company_financials_ids))
                        .delete()
                    )
                    info_message = f"The {delete_result} derived financials data from "
                    info_message += f"{len(db_company_financials_ids)} has deleted from database."
                    self.__logger.info(info_message)

                    delete_result = (
                        session.query(DbFinancials).filter(DbFinancials.id.in_(db_company_financials_ids)).delete()
                    )
                    info_message = f"The {delete_result} financials data from "
                    info_message += f"{len(db_company_financials_ids)} has deleted from database."
                    self.__logger.info(info_message)

                delete_result = session.query(DbCompany).filter(DbCompany.id.in_(removed_companies)).delete()
                info_message = f"The {delete_result} companies data from "
                info_message += f"{len(removed_companies)} has deleted from database."
                self.__logger.info(info_message)

            return None
