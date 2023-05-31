from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.containers import Container
from api.data_transfer_objects.dto_user import DtoUser
from api.service_layer.user_service import UserService

router = APIRouter(prefix="/admin")


@router.get(
    "/users",
    tags=["User"],
    summary="get all users",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_users(
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        result = user_service.get_all_entities()
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(
        content=jsonable_encoder(result),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/users/{id}",
    tags=["User"],
    summary="get user by id",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user_by_id(
    id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        result = user_service.get_entity_by_id(id=id)
        return (
            JSONResponse(
                content=jsonable_encoder(result),
                status_code=status.HTTP_200_OK,
            )
            if result is not None
            else Response(status_code=status.HTTP_404_NOT_FOUND)
        )
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/users", tags=["User"], summary="create user", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    entity: DtoUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user_service.create_entity(entity=entity)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/users/many",
    tags=["User"],
    summary="create users",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_users(
    entities: List[DtoUser],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user_service.bulk_save_entities(entities=entities)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)
