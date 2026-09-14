from celery import Task
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from croniter import croniter

from app.db.session import SessionLocal
from app.models.automation import Automation
# from app.services.execution import execute_automation
from app.workers.celery_app import celery_app
from app.services.execution import (run_execution, create_pending_execution)
from app.services import execution as execution_service
from app.models.automation_execution import AutomationExecution
from app.services.scheduler import (get_scheduled_automations, calculate_next_run)

class DatabaseTask(Task):

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

@celery_app.task
def execute_automation_task(
    execution_id: int,
) -> int:

    db: Session = SessionLocal()

    try:
        execution = db.get(
            AutomationExecution,
            execution_id,
        )

        if execution is None:
            raise ValueError(
                f"Automation {execution_id} not found"
            )
        
        automation = db.get(
            Automation,
            execution.automation_id,
        )

        if automation is None:
            raise ValueError(
                f"Automation {execution.automation_id} not found"
            )

        execution_service.run_execution(
            db,
            execution,
            automation,
        )

        return execution.id

    finally:
        db.close()

@celery_app.task
def check_scheduled_automations() -> int:

    db: Session = SessionLocal()

    try:
        automations = get_scheduled_automations(db)
        now = datetime.now(timezone.utc)

        queued_count = 0

        for automation in automations:
            if automation.next_run_at is None:
                if automation.schedule_cron:
                    automation.next_run_at = calculate_next_run(
                        automation.schedule_cron,
                        now,
                    )

                    db.commit()

                continue

            if automation.next_run_at > now:
                continue

            execution = create_pending_execution(db, automation.id)
            execute_automation_task.delay(execution.id)

            db.commit()

            queued_count += 1

            # cron = croniter(
            #     automation.schedule_cron,
            #     now,
            # )
            # previous_run = cron.get_prev(datetime)
            # if previous_run <= now:
            #     execution = create_pending_execution(db, automation.id)
            #     execute_automation_task.delay(execution.id)


        return queued_count
    
    finally:
        db.close()


@celery_app.task
def test_task() -> str:
    return "Celery worker is working"