from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.execution import AutomationExecutionResponse
from app.services import automation as automation_service
from app.services import execution as execution_service
from app.schemas.execution import (
    AutomationExecutionResponse,
)
from app.repositories import execution as execution_repository
from app.workers.tasks import execute_automation_task
from app.services.execution import create_pending_execution
from app.workers.tasks import execute_automation_task
from app.services import execution_log as execution_log_service
from app.schemas.execution import ExecutionLogResponse


router = APIRouter(
    prefix="/automations",
    tags=["Automation Execution"],
)


@router.post(
    "/automations/{automation_id}/execute",
    response_model=AutomationExecutionResponse,
)
def execute_automation(
    automation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    automation = automation_service.get_automation(
        db,
        automation_id,
        current_user.id,
    )

    if not automation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation not found",
        )

    execution = create_pending_execution(
        db,
        automation_id,
    )

    execute_automation_task.delay(
        execution.id,
    )

    return execution

@router.get(
    "/{automation_id}/executions",
    response_model=list[AutomationExecutionResponse],
)
def list_executions(
    automation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    automation = automation_service.get_automation(
        db,
        automation_id,
        current_user.id,
    )

    if not automation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation not found",
        )

    return execution_repository.get_executions(
        db,
        automation_id,
    )

@router.get(
    "/{automation_id}/executions/{execution_id}",
    response_model=AutomationExecutionResponse,
)
def get_execution(
    automation_id: int,
    execution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    automation = automation_service.get_automation(
        db,
        automation_id,
        current_user.id,
    )

    if not automation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation not found",
        )

    # execution = execution_repository.get_execution(
    #     db,
    #     execution_id,
    # )

    task = execute_automation_task.delay(
        automation.id
    )

    if (
        not task
        or task.automation_id != automation_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found",
        )

    return task

@router.get(
    "/automations/{automation_id}/executions/{execution_id}/logs",
    response_model=list[ExecutionLogResponse],
)
def get_execution_logs(
    automation_id: int,
    execution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    automation = automation_service.get_automation(
        db,
        automation_id,
        current_user.id,
    )

    if automation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation not found",
        )

    execution = execution_repository.get_execution(db, execution_id,)

    if (
        execution is None
        or execution.automation_id != automation_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found",
        )

    return execution_log_service.get_logs( db, execution_id, )