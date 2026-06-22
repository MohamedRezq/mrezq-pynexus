from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class DomainService(ABC, Generic[T]):  # noqa: UP046
    """
    Base class for domain services.
    Provides consistent logging + error handling via the Template Method pattern.
    Subclasses only implement execute() — run() wraps it with logging.
    """

    def __init__(self) -> None:
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def execute(self, *args: object, **kwargs: object) -> T:
        """Override this with actual business logic."""
        ...

    async def run(self, *args: object, **kwargs: object) -> T:
        """Template method — logs start/end, catches and re-raises on failure."""
        self._log.info("starting %s", self.__class__.__name__)
        try:
            result: T = await self.execute(*args, **kwargs)
            self._log.info("completed %s", self.__class__.__name__)
            return result
        except Exception as exc:
            self._log.error("failed %s: %s", self.__class__.__name__, exc, exc_info=True)
            raise
