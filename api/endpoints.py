from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.api_key import APIKey

from api.auth import api_key_security
from api.containers import Container
from api.service_layer.user_service import UserService

router = APIRouter(prefix="/api")


@inject
async def __get_user_id_by_api_key(
    user_service: UserService = Depends(Provide[Container.user_service]),
    api_key: APIKey = Depends(api_key_security),
):
    user_id = user_service.get_user_id_by_api_key(api_key)
    if user_id is not None:
        return user_id
    raise HTTPException(detail="Wrong api key", status_code=status.HTTP_403_FORBIDDEN)
