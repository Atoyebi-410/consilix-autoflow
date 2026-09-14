from datetime import datetime, timezone
from sqlalchemy.orm import Session
import time

from app.models.automation import Automation
from app.models.automation_execution import AutomationExecution
from app.models.step_excutions import StepExecution
from app.repositories import execution as execution_repository
from app.workflow import WorkflowEngine, create_default_registry
from app.models.automation_execution import AutomationExecution
from app.services import execution_log as execution_log_service


def run_execution(
    db: Session,
    execution: AutomationExecution,
    automation: Automation,
) -> AutomationExecution:

    # execution = AutomationExecution(
    #     automation_id=automation.id,
    #     status="pending",
    # )

    # execution_repository.create_execution(
    #     db,
    #     execution,
    # )

    # execution.status = "running"
    # execution.started_at = datetime.now(timezone.utc)
    execution_log_service.log(
        db,
        execution.id,
        "Automation execution started",
    )

    execution.status = "running"
    execution.started_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(execution)

    engine = WorkflowEngine(
        create_default_registry()
    )

    try:
        for step in automation.steps:

            if not step.is_enabled:
                execution_log_service.log(
                    db,
                    execution.id,
                    f"Starting step {step.position}: {step.name}",
                )
                step_execution = StepExecution(
                    execution_id=execution.id,
                    step_id=step.id,
                    position=step.position,
                    attempt_number=1,
                    status="skipped",
                    output={"message": "Step is disabled"},
                )

                execution_repository.create_step_execution(
                    db,
                    step_execution,
                )

                execution_log_service.log(
                    db,
                    execution.id,
                    f"Step {step.position} skipped because it is disabled",
                )

                continue

            max_attempts = 1

            if step.retry_enabled:
                max_attempts += step.max_retries

            step_succeeded = False

            for attempt_number in range(1, max_attempts+1):
                execution_log_service(
                    db,
                    execution.id,
                    f"Starting step {step.position}: "
                    f"{step.name} "
                    f"(attempt {attempt_number}/{max_attempts})",
                )

                step_execution = StepExecution(
                    execution_id=execution.id,
                    step_id=step.id,
                    position=step.position,
                    attempt_number=attempt_number,
                    status="running",
                    started_at=datetime.now(timezone.utc),
                )

                execution_repository.create_step_execution(
                    db,
                    step_execution,
                )

                try:
                    adapter = engine.registry.get(
                        step.step_type
                    )

                    result = engine.execute_step(step)

                    step_execution.status = "completed"
                    step_execution.output = result
                    step_execution.completed_at = (
                        datetime.now(timezone.utc)
                    )

                    db.commit()

                    execution_log_service.log(
                        db,
                        execution.id,
                        f"Step {step.position} completed successfully "
                        f"on attempt {attempt_number}",
                    )

                    step_succeeded = True
                    break


                except Exception as exc:
                    step_execution.status = "failed"
                    step_execution.error_message = str(exc)
                    step_execution.completed_at = (
                        datetime.now(timezone.utc)
                    )

                    db.commit()

                    execution_log_service.log(
                        db,
                        execution.id,
                        f"Step {step.position} failed on "
                        f"attempt {attempt_number}: {exc}",
                        level="ERROR",
                    )

                    if attempt_number < max_attempts:
                        execution_log_service.log(
                            db,
                            execution.id,
                            f"Retrying step {step.position} "
                            f"after {step.retry_delay_seconds} seconds",
                        )

                        time.sleep(step.retry_delay_seconds)

            if not step_succeeded: 

                execution.status = "failed"
                execution.error_message = (
                    f"Step {step.position} failed after "
                    f"{max_attempts} attempt(s)"
                )
                execution.completed_at = (datetime.now(timezone.utc))

                db.commit()
                db.refresh(execution)

                return execution

        execution.status = "completed"
        execution.completed_at = datetime.now(timezone.utc)

        execution_log_service.log(
            db,
            execution.id,
            "Automation execution completed",
        )

        db.commit()
        db.refresh(execution)

        return execution

    except Exception as exc:
        execution.status = "failed"
        execution.error_message = str(exc)
        execution.completed_at = datetime.now(timezone.utc)

        execution_log_service.log(
            db,
            execution.id,
            f"Automation execution failed: {exc}",
            level="ERROR",
        )

        db.commit()
        db.refresh(execution)

        return execution

def create_pending_execution(
        db: Session,
        automation_id: int,
) -> AutomationExecution:

    execution = AutomationExecution(
        automation_id=automation_id,
        status="pending",
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution

