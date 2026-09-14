from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Automation(Base):
    __tablename__ = "automations"

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'active', 'paused', 'archived')",
            name="ck_automations_status"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="automations")
    steps = relationship(
        "AutomationStep", 
        back_populates="automation", 
        cascade="all, delete-orphan",
        order_by="AutomationStep.position"
    )

    executions = relationship(
        "AutomationExecution",
        back_populates="automation",
        cascade="all, delete-orphan",
    )

    schedule_enabled: Mapped[bool] = mapped_column(
    default=False,
    nullable=False,
    )

    schedule_cron: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    schedule_timezone: Mapped[str] = mapped_column(
        String(100),
        default="UTC",
        nullable=False,
    )
    next_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )