from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from shared.domain.enums import UserRole
from shared.domain.permissions import has_permission
from shared.utils.datetime_utils import _utcnow


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str | None = None
    hashed_password: str | None = None
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool = True
    last_login_at: datetime | None = None
    created_at: datetime = field(default_factory=_utcnow)

    """ Domain Behaviors"""

    def deactivate(self) -> None:
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = True

    def activate(self) -> None:
        if self.is_active:
            raise ValueError("User is already active")
        self.is_active = False

    def record_login(self) -> None:
        self.last_login_at = _utcnow()

    def has_permission(self, action: str) -> bool:
        return has_permission(self.role, action)
