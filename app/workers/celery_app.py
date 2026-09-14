from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "consilix-autoflow",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # beat_scheduler = "celery.beat:PersistentScheduler"
)

celery_app.conf.beat_schedule = {
    "check-scheduled-automations-every-minute": {
        "task": "app.workers.tasks.check_scheduled_automations",
        "schedule": 60.0,
    },
}