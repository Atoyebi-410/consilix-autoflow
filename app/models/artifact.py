from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(primary_key=True)

    execution_id: Mapped[int] = mapped_column(
        ForeignKey(
            "automation_executions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    step_execution_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "step_executions.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    artifact_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    content_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    execution = relationship(
        "AutomationExecution",
        back_populates="artifacts",
    )

    step_execution = relationship(
        "StepExecution",
    )