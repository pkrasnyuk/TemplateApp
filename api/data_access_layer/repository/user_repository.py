from contextlib import AbstractContextManager
from typing import Callable, List, Optional

from sqlalchemy.orm import Session

from api.data_transfer_objects.dto_user import DtoUser
from core.data_access_layer.repository.base_repository import BaseRepository
from core.domain.user import DbUser


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory=session_factory, db_model=DbUser)  # type: ignore

    def create(self, item: DtoUser) -> None:
        return super().create(item)

    def bulk_save(self, items: List[DtoUser]) -> None:
        return super().bulk_save(items)

    def get_user_id_by_api_key(self, api_key: str) -> Optional[int]:
        with self.session_factory() as session:
            user = session.query(DbUser).filter(DbUser.api_key == api_key).first()
            return user.id if user is not None else None
