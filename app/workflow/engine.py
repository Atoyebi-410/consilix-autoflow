from typing import Any

from app.models.automation import Automation
from app.models.automation_step import AutomationStep
from app.workflow.registry import AdapterRegistry


class WorkflowEngine:

    def __init__(
        self,
        registry: AdapterRegistry,
    ) -> None:
        self.registry = registry

    def execute_step(
        self,
        step: AutomationStep,
    ) -> dict[str, Any]:

        adapter = self.registry.get(
            step.step_type
        )

        return adapter.execute(
            step.config
        )

    def execute(
        self,
        automation: Automation,
    ) -> list[dict[str, Any]]:

        results: list[dict[str, Any]] = []

        for step in automation.steps:

            if not step.is_enabled:
                results.append(
                    {
                        "step_id": step.id,
                        "status": "skipped",
                    }
                )
                continue

            result = self.execute_step(step)

            results.append(
                {
                    "step_id": step.id,
                    "position": step.position,
                    "step_type": step.step_type,
                    "result": result,
                }
            )

        return results