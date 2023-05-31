from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey

from api.auth import api_key_security
from api.containers import Container
from api.data_transfer_objects.dto_pricing import DtoPricing
from api.service_layer.pricing_service import PricingService
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


@router.post(
    "/pricings",
    tags=["Pricings"],
    summary="create pricing request",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def pricing_request(
    entities: List[DtoPricing],
    pricing_service: PricingService = Depends(Provide[Container.pricing_service]),
    user_id: int = Depends(__get_user_id_by_api_key),
):
    try:
        pricing_service.request_processing(entities, user_id)
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_200_OK)
