import json

from pydantic import BaseModel, ConfigDict

from core.domain.entity import DbEntity
from core.helpers.common import default_json_dumps


class DtoEntity(BaseModel):
    pass

    def entity_preprocessing(self):
        return json.loads(json.dumps(self.model_dump(by_alias=True), default=default_json_dumps))

    def _is_identical_to_db_entity(self, entity: DbEntity):
        return True

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, from_attributes=True)
