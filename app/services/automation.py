from sqlalchemy.orm import Session
from app.models.automation import Automation
from app.repositories import automation as automation_repository
from app.schemas.automation import AutomationCreate, AutomationUpdate

def create_automation(
        db: Session,
        user_id: int,
        data: AutomationCreate,
) -> Automation:
    automation = Automation(
        name=data.name,
        description=data.description,
        user_id=user_id,
    )

    return automation_repository.create_automation(
        db,
        automation,
    )

def get_automation(
        db: Session,
        automation_id: int,
        user_id: int,
) -> Automation | None:
    return automation_repository.get_automation(
        db,
        automation_id,
        user_id,
    )

def get_automations(
        db: Session,
        user_id: int,
) -> list[Automation]:
    return automation_repository.get_automations(
        db,
        user_id,
    )

def update_automation(
        db: Session,
        automation: Automation,
        data: AutomationUpdate,
) -> Automation:
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(automation, field, value)

    db.commit()
    db.refresh(automation)

def delete_automation(
        db: Session,
        automation: Automation,
) -> None:
    automation_repository.delete_automation(
        db,
        automation,
    )