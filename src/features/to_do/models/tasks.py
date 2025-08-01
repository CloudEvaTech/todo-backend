import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base


class ToDoItem(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    # Use string reference for relationship
    user: Mapped["User"] = relationship("User", back_populates="tasks", lazy="selectin")

    # Status relationship
    status: Mapped["Status"] = relationship(
        "Status", back_populates="task", uselist=False
    )


class Status(Base):
    __tablename__ = "statuses"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    completed: Mapped[bool] = mapped_column(default=False)

    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"))

    # Relationship with back_populates
    task: Mapped["ToDoItem"] = relationship("ToDoItem", back_populates="status")
