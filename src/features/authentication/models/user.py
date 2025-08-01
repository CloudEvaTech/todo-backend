from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, LargeBinary
import uuid
import datetime as dt
from sqlalchemy import DateTime
import bcrypt
from src.core.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    _password: Mapped[bytes] = mapped_column("password", LargeBinary(128), nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc))
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))

    # Use string reference for relationship
    tasks: Mapped[List["ToDoItem"]] = relationship("ToDoItem", back_populates="user", lazy="selectin")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, value: str) -> bool:
        return bcrypt.checkpw(value.encode('utf-8'), self._password)