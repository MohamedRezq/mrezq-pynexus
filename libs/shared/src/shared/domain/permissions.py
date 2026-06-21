from shared.domain.enums import UserRole

ROLE_PERMISSIONS: dict[UserRole, set[str]] = {
    UserRole.VIEWER: {"document:read", "client:read"},
    UserRole.ANALYST: {"document:read", "document:upload", "client:read", "ai:query"},
    UserRole.RISK_MANAGER: {
        "document:read",
        "document:upload",
        "client:read",
        "client:write",
        "ai:query",
        "ml:score",
    },
    UserRole.ADMIN: {"*"},  # wildcard = all
}


def has_permission(role: UserRole | None, action: str) -> bool:
    if role is None:
        return False
    else:
        user_permissions = ROLE_PERMISSIONS.get(role, set())
        return "*" in user_permissions or action in user_permissions
