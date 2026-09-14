from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.artifact import Artifact


def create_artifact(
    db: Session,
    artifact: Artifact,
) -> Artifact:
    db.add(artifact)
    db.commit()
    db.refresh(artifact)

    return artifact


def get_artifacts(
    db: Session,
    execution_id: int,
) -> list[Artifact]:
    return list(
        db.scalars(
            select(Artifact)
            .where(
                Artifact.execution_id == execution_id
            )
            .order_by(Artifact.created_at)
        )
    )