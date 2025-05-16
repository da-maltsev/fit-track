from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, event, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[Any]
    __name__: str  # type: ignore[misc]

    # Generate __tablename__ automatically
    @declared_attr  # type: ignore[arg-type]
    def __tablename__(self) -> str:
        return self.__name__.lower()

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


@event.listens_for(Base, "before_update", propagate=True)
def receive_before_update(_mapper: Any, _connection: Any, target: Base) -> None:
    """Set updated_at field to current timestamp before update."""
    target.updated_at = datetime.now(UTC)
