from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.automation import (
    AutomationCreate,
    AutomationResponse,
    AutomationUpdate,
)
from app.services import automation as automation_service

router = APIRouter(
    prefix="/automation",
    tags=["Automations"],
)

@router.post(
    "",
    response_model=AutomationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_automation(
    data: AutomationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return automation_service.create_automation(
        db,
        current_user.id,
        data,
    )

@router.get(
    "",
    response_model=list[AutomationResponse],
)
def list_automations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return automation_service.get_automations(
        db,
        current_user.id,
    )

@router.get(
    "/(automation_id)",
    response_model=AutomationResponse,
)
def get_automation(
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

    return automation