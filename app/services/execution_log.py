from sqlalchemy.orm import Session
from app.models.execution_log import ExecutionLog
from app.repositories import execution_log as log_repository

def log(
        db: Session,
        execution_id: int,
        message: str,
        level: str = "INFO",
) -> ExecutionLog:

    return log_repository.create_log(
        db=db,
        execution_id=execution_id,
        level=level,
        message=message,
    )

def get_logs(
        db: Session,
        execution_id: int,
) -> list[ExecutionLog]:

    return log_repository.get_logs(
        db,
        execution_id,
    )