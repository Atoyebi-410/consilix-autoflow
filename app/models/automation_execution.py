from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AutomationExecution(Base):
    __tablename__ = "automation_executions"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed', 'cancelled')",
            name="ck_automation_executions_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    automation_id: Mapped[int] = mapped_column(
        ForeignKey("automations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    automation = relationship(
        "Automation",
        back_populates="executions",
    )

    step_executions = relationship(
        "StepExecution",
        back_populates="execution",
        cascade="all, delete-orphan",
        order_by="StepExecution.position",
    )

    logs = relationship(
        "ExecutionLog",
        back_populates="execution",
        cascade="all, delete-orphan",
        order_by="ExecutionLog.created_at",
    )

    artifacts = relationship(
        "Artifact",
        back_populates="execution",
        cascade="all, delete-orphan",
    )