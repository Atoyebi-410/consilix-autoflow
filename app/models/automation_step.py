from datetime import datetime
from sqlalchemy import (
    Boolean, 
    CheckConstraint, 
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    func
    )
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base 

class AutomationStep(Base):
    __tablename__ = "automation_steps"

    __table_args__ = (
        CheckConstraint(
            "step_type IN ('browser', 'http', 'email', 'delay', 'condition')",
            name="ck_automation_steps_step_type",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    automation_id: Mapped[int] = mapped_column(
        ForeignKey("automations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    step_type: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    retry_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    retry_delay_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
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

    automation = relationship("Automation", back_populates="steps")