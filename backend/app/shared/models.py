"""Centralized ORM models = the shared persistence contract.

Kept in one module (not per-context) so every teammate imports the same table
definitions and Alembic has a single migration head. The domain entities that
each context maps to/from live in their own `domain/` packages.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.db import Base

# Canonical states required by the technical test (PDF).
STATUS_PENDING = "pendiente"
STATUS_PROCESSED = "procesado"
STATUS_FAILED = "fallido"

# Transaction kinds in the unified model.
KIND_BOOK = "libro"
KIND_SALE = "venta"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), default="")
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(20), default="Lector")  # Admin | Editor | Lector
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    settings: Mapped["UserSettings | None"] = relationship(back_populates="user", uselist=False)


class Transaction(Base):
    """Unified transactional core. `tipo` discriminates a generated book from a sale."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(20), index=True)  # libro | venta
    estado: Mapped[str] = mapped_column(String(20), default=STATUS_PENDING, index=True)
    sub_estado: Mapped[str | None] = mapped_column(String(20), nullable=True)  # buscando | resumiendo
    idempotency_key: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # tipo == "libro"
    titulo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    precio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    estilo: Mapped[str | None] = mapped_column(String(30), nullable=True)
    resumen: Mapped[str | None] = mapped_column(Text, nullable=True)
    log: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)

    # tipo == "venta"
    monto: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    libro_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("transactions.id"), nullable=True, index=True
    )


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    default_source: Mapped[str] = mapped_column(String(30), default="Wikipedia (ES)")
    default_style: Mapped[str] = mapped_column(String(30), default="Formal")

    user: Mapped[User] = relationship(back_populates="settings")


class AssistantLog(Base):
    __tablename__ = "assistant_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    input_text: Mapped[str] = mapped_column(Text)
    output_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    model: Mapped[str] = mapped_column(String(50), default="fake")
    tokens: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ok")  # ok | error
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
