from app.adapters.base import BaseAdapter
from app.adapters.browser import BrowserAdapter
from app.adapters.email import EmailAdapter
from app.adapters.http import HTTPAdapter


class AdapterRegistry:

    def __init__(self) -> None:
        self._adapters: dict[str, BaseAdapter] = {}

    def register(self, adapter: BaseAdapter) -> None:
        self._adapters[adapter.step_type] = adapter

    def get(self, step_type: str) -> BaseAdapter:
        adapter = self._adapters.get(step_type)

        if adapter is None:
            raise ValueError(
                f"No adapter registered for step type: {step_type}"
            )

        return adapter


def create_default_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    
    registry.register(BrowserAdapter())
    registry.register(HTTPAdapter())
    registry.register(EmailAdapter())

    return registry