"""Domain errors for the transactions context.

These are transport-agnostic; the HTTP entrypoint maps them to status codes.
"""


class TransactionError(Exception):
    """Base class for transactions domain errors."""


class BookNotFoundError(TransactionError):
    """The referenced book does not exist."""


class BookNotSellableError(TransactionError):
    """The book cannot be sold (not processed or has no price)."""
