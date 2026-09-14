from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.automation_step import AutomationStep


def create_step(
    db: Session,
    step: AutomationStep,
) -> AutomationStep:
    db.add(step)
    db.commit()
    db.refresh(step)

    return step


def get_step(
    db: Session,
    step_id: int,
    automation_id: int,
) -> AutomationStep | None:
    return db.scalar(
        select(AutomationStep).where(
            AutomationStep.id == step_id,
            AutomationStep.automation_id == automation_id,
        )
    )


def get_steps(
    db: Session,
    automation_id: int,
) -> list[AutomationStep]:
    return list(
        db.scalars(
            select(AutomationStep)
            .where(
                AutomationStep.automation_id == automation_id
            )
            .order_by(AutomationStep.position)
        )
    )


def delete_step(
    db: Session,
    step: AutomationStep,
) -> None:
    db.delete(step)
    db.commit()