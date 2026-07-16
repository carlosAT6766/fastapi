"""Auth domain: roles and invariants independent of framework/persistence."""

# Canonical user roles used across the auth context.
ROLE_ADMIN = "Admin"
ROLE_EDITOR = "Editor"
ROLE_READER = "Lector"

VALID_ROLES = frozenset({ROLE_ADMIN, ROLE_EDITOR, ROLE_READER})

# Default password assigned to users created by an admin (T13).
DEFAULT_USER_PASSWORD = "changeme123"


def is_valid_role(role: str) -> bool:
    """Return whether the given role is one of the accepted roles."""
    return role in VALID_ROLES
