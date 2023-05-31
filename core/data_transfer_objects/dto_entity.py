import json

from pydantic import BaseModel

from core.domain.entity import DbEntity
from core.helpers.common import default_json_dumps


class DtoEntity(BaseModel):
    pass

    def entity_preprocessing(self):
        return json.loads(json.dumps(self.dict(by_alias=True), default=default_json_dumps))

    def _is_identical_to_db_entity(self, entity: DbEntity):
        return True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        require_by_default = False
