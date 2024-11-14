from pydantic import BaseModel, ConfigDict, Field


class SchedulerJob(BaseModel):
    name: str = Field(default="")
    crontab: str = Field(default="* */12 * * *")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
