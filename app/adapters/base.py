from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):

    @property
    @abstractmethod
    def step_type(self) -> str:
        """Return the step type handled by this adapter."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, config: dict[str, Any]) -> dict[str, Any]:
        """Execute a workflow step."""
        raise NotImplementedError