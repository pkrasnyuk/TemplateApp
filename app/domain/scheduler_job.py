from pydantic import BaseConfig, BaseModel, Field


class SchedulerJob(BaseModel):
    name: str = Field(default="")
    crontab: str = Field(default="* */12 * * *")

    class Config(BaseConfig):
        allow_population_by_field_name = True
