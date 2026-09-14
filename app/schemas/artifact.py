from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArtifactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    execution_id: int
    step_execution_id: int | None
    artifact_type: str
    name: str
    file_path: str | None
    content_type: str | None
    created_at: datetime