from typing import List, Optional
from api.data_access_layer.repository.user_repository import UserRepository
from api.data_transfer_objects.dto_user import DtoUser
from core.domain.user import User


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def get_all_entities(self) -> List[Optional[User]]:
        return self.__repository.get_all()
    
    def get_entity_by_id(self, id: int) -> Optional[User]:
        return self.__repository.get_by_id(id)

    def create_entity(self, entity: DtoUser) -> None:
        return self.__repository.create(item=entity)
    
    def bulk_save_entities(self, entities: List[DtoUser]) -> None:
        return self.__repository.bulk_save(items=entities)
    
    def get_user_id_by_api_key(self, api_key: str) -> Optional[int]:
        return self.__repository.get_user_id_by_api_key(api_key=api_key)
