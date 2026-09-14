from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class StepType(str, Enum):
    BROWSER = "browser"
    HTTP = "http"
    EMAIL = "email"
    DELAY = "delay"
    CONDITION = "condition"

class AutomationStepCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    step_type: StepType
    position: int = Field(ge=1)
    config: dict[str, Any] = Field(default_factory=dict)
    is_enabled: bool = True

    retry_enabled: bool = False

    max_retries: int = Field(
        default=0,
        ge=0,
    )

    retry_delay_seconds: int = Field(
        default=0,
        ge=0,
    )

class AutomationStepUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    step_type: StepType | None = None
    position: int | None = Field(default=None, ge=1)
    config: dict[str, Any] | None = None
    is_enabled: bool | None = None 

    retry_enabled: bool | None = None

    max_retries: int | None = Field(
        default=None,
        ge=0,
    )

    retry_delay_seconds: int | None = Field(
        default=None,
        ge=0,
    )

class AutomationStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    automation_id: int
    name: str
    step_type: str
    position: int
    config: dict[str, Any]
    is_enabled: bool
    created_at: datetime
    updated_at: datetime
    retry_enabled: bool
    max_retries: int
    retry_delay_seconds: int