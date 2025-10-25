from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import User
from .agent_keypair import AgentKeypair
from .base import Base, CreatedAt


class AgentStatus(StrEnum):
    DOWN = "down"
    UP = "up"


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column()
    port: Mapped[int] = mapped_column()
    rhost: Mapped[str] = mapped_column()
    rport: Mapped[int] = mapped_column()
    suspended_since: Mapped[datetime | None] = mapped_column()
    status: Mapped[AgentStatus] = mapped_column()
    created_at: Mapped[CreatedAt]

    keypair_id: Mapped[int] = mapped_column(ForeignKey("agent_keypair.id"))
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    keypair: Mapped[AgentKeypair] = relationship(lazy="selectin")
    created_by_user: Mapped[User] = relationship()
