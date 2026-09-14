from typing import Any

from app.adapters.base import BaseAdapter


class EmailAdapter(BaseAdapter):
    @property
    def step_type(self) -> str:
        return "email"

    def execute(self, config: dict[str, Any]) -> dict[str, Any]:
        recipient = config.get("to")
        subject = config.get("subject")

        if not recipient:
            raise ValueError("Email step requires a recipient")

        return {
            "status": "success",
            "message": "Email step received",
            "to": recipient,
            "subject": subject,
        }