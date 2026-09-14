from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.automation_step import (
    AutomationStepCreate,
    AutomationStepResponse,
    AutomationStepUpdate,
)
from app.services import automation_step as step_service
from app.services import automation as automation_service


router = APIRouter(
    prefix="/automations/{automation_id}/steps",
    tags=["Automation Steps"],
)

@router.post(
    "",
    response_model=AutomationStepResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_step(
    automation_id: int,
    data: AutomationStepCreate,
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

    return step_service.create_step(
        db,
        automation_id,
        data,
    )

@router.get(
    "",
    response_model=list[AutomationStepResponse],
)
def list_steps(
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

    return step_service.get_steps(
        db,
        automation_id,
    )

@router.get(
    "/{step_id}",
    response_model=AutomationStepResponse,
)
def get_step(
    automation_id: int,
    step_id: int,
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

    step = step_service.get_step(
        db,
        step_id,
        automation_id,
    )

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation step not found",
        )

    return step

@router.patch(
    "/{step_id}",
    response_model=AutomationStepResponse,
)
def update_step(
    automation_id: int,
    step_id: int,
    data: AutomationStepUpdate,
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

    step = step_service.get_step(
        db,
        step_id,
        automation_id,
    )

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation step not found",
        )

    return step_service.update_step(
        db,
        step,
        data,
    )

@router.delete(
    "/{step_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_step(
    automation_id: int,
    step_id: int,
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

    step = step_service.get_step(
        db,
        step_id,
        automation_id,
    )

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation step not found",
        )

    step_service.delete_step(
        db,
        step,
    )