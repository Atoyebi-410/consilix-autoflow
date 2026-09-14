from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.execution_log import ExecutionLog

def create_log(
        db: Session,
        execution_id: int,
        level: str,
        message: str,
) -> ExecutionLog:

    log = ExecutionLog(
        execution_id=execution_id,
        level=level,
        message=message,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

def get_logs(
        db: Session,
        execution_id: int,
) -> list[ExecutionLog]:
 
    result = db.scalars(
        select(ExecutionLog)
        .where(ExecutionLog.execution_id == execution_id)
        .order_by(ExecutionLog.created_at)
    )

    return list(result)