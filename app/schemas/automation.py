from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator

class AutomationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    schedule_enabled: bool = False
    schedule_cron: str | None = None
    schedule_timezone: str = "UTC"

    @model_validator(mode="after")
    def validate_schedule(self):
        if self.schedule_enabled and not self.schedule_cron:
            raise ValueError("schedule_cron is required when scheduling is enabled")

        return self

class AutomationStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"

class AutomationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: AutomationStatus | None = None
    schedule_enabled: bool | None = None
    schedule_cron: str | None = None
    schedule_timezone: str | None = None

class AutomationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    status: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    schedule_enabled: bool
    schedule_cron: str | None
    schedule_timezone: str
