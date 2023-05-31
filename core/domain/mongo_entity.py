from datetime import datetime, timezone

from bson.objectid import ObjectId
from pydantic import BaseConfig, BaseModel, Field

from core.domain.py_object_id import PyObjectId


class MongoEntity(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        require_by_default = False
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            ObjectId: str,
        }
