from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.automation_execution import AutomationExecution
from app.models.step_excutions import StepExecution

def create_execution(
        db: Session,
        execution: AutomationExecution,
) -> AutomationExecution:
    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution

def get_execution(
        db: Session,
        execution_id: int,
) -> AutomationExecution | None:
    return db.get(
        AutomationExecution,
        execution_id,
    )

def get_executions(
        db: Session,
        automation_id: int,
) -> list[AutomationExecution]:
    return list(
        db.scalars(
            select(AutomationExecution)
            .where(
                AutomationExecution.automation_id == automation_id
            )
            .order_by(
                AutomationExecution.created_at.desc()
            )
        )
    )

def create_step_execution(
        db: Session,
        step_execution: StepExecution,
) -> StepExecution:
    db.add(step_execution)
    db.commit()
    db.refresh(step_execution)

    return step_execution