from datetime import datetime, timezone

from bson.objectid import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from core.domain.py_object_id import PyObjectId


class MongoEntity(BaseModel):
    id: PyObjectId = Field(default=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            ObjectId: str,
        },
    )
