from pydantic import Field, field_validator

from core.data_transfer_objects.dto_entity import DtoEntity


class DtoUser(DtoEntity):
    name: str = Field(max_length=32)
    api_key: str = Field(max_length=64)

    @field_validator("name", mode="after")
    def name_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v
