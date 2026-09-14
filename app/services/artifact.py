from sqlalchemy.orm import Session

from app.models.artifact import Artifact
from app.repositories import artifact as artifact_repository


def create_artifact(
    db: Session,
    execution_id: int,
    artifact_type: str,
    name: str,
    file_path: str | None = None,
    content_type: str | None = None,
    step_execution_id: int | None = None,
) -> Artifact:

    artifact = Artifact(
        execution_id=execution_id,
        step_execution_id=step_execution_id,
        artifact_type=artifact_type,
        name=name,
        file_path=file_path,
        content_type=content_type,
    )

    return artifact_repository.create_artifact(
        db,
        artifact,
    )


def get_artifacts(
    db: Session,
    execution_id: int,
) -> list[Artifact]:
    return artifact_repository.get_artifacts(
        db,
        execution_id,
    )