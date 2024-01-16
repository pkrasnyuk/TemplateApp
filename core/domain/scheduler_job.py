from pydantic import BaseModel, ConfigDict, Field


class SchedulerJob(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(default="")
    crontab: str = Field(default="* */12 * * *")
