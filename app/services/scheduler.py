from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.automation import Automation
from datetime import datetime, timezone
from croniter import croniter

def get_scheduled_automations(
        db: Session,
) -> list[Automation]:

    return list(
        db.scalars(
            select(Automation)
            .where(
                Automation.schedule_enabled.is_(True),
                Automation.status == "active",
                Automation.schedule_cron.is_not(None),
            )
        )
    )

def calculate_next_run(
        cron_expression: str,
        base_time: datetime | None = None,
) -> datetime:

    if base_time is None:
        base_time = datetime.now(timezone.utc)

    cron = croniter(
        cron_expression,
        base_time,
    )

    return cron.get_next(datetime)