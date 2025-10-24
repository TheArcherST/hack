from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(unique=True)
    ssh_public_key: Mapped[str] = mapped_column(unique=True)
    suspended_since: Mapped[datetime | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
