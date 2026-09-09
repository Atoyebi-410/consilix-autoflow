from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.automation import Automation

def create_automation(
        db: Session,
        automation: Automation,
) -> Automation:
    db.add(automation)
    db.commit()
    db.refresh(automation)

    return automation

def get_automation(
        db: Session,
        automation_id: int,
        user_id: int,
) -> Automation | None:
    return db.scalar(
        select(Automation).where(
            Automation.id == automation_id,
            Automation.user_id == user_id,
        )
    )

def get_automations(
        db: Session,
        user_id: int,
) -> list[Automation]:
    return list(
        db.scalars(
            select(Automation)
            .where(Automation.user_id == user_id)
            .order_by(Automation.created_at.desc())
        )
    )

def delete_automation(
        db: Session,
        automation: Automation,
) -> None:
    db.delete(automation)
    db.commit()
    