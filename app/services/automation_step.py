from sqlalchemy.orm import Session

from app.models.automation_step import AutomationStep
from app.repositories import automation_step as step_repository
from app.schemas.automation_step import (
    AutomationStepCreate,
    AutomationStepUpdate,
)


def create_step(
    db: Session,
    automation_id: int,
    data: AutomationStepCreate,
) -> AutomationStep:

    step = AutomationStep(
        automation_id=automation_id,
        name=data.name,
        step_type=data.step_type.value,
        position=data.position,
        config=data.config,
        is_enabled=data.is_enabled,
        retry_enabled=data.retry_enabled,
        max_retries=data.max_retries,
        retry_delay_seconds=data.retry_delay_seconds,
    )

    return step_repository.create_step(db, step)


def get_step(
    db: Session,
    step_id: int,
    automation_id: int,
) -> AutomationStep | None:

    return step_repository.get_step(
        db,
        step_id,
        automation_id,
    )


def get_steps(
    db: Session,
    automation_id: int,
) -> list[AutomationStep]:

    return step_repository.get_steps(
        db,
        automation_id,
    )


def update_step(
    db: Session,
    step: AutomationStep,
    data: AutomationStepUpdate,
) -> AutomationStep:

    update_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if "step_type" in update_data:
        update_data["step_type"] = update_data["step_type"].value

    for field, value in update_data.items():
        setattr(step, field, value)

    db.commit()
    db.refresh(step)

    return step


def delete_step(
    db: Session,
    step: AutomationStep,
) -> None:

    step_repository.delete_step(db, step)