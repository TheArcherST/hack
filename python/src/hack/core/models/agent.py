from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .agent_keypair import AgentKeypair
from .base import Base, CreatedAt


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(unique=True)
    port: Mapped[int] = mapped_column()
    rhost: Mapped[str] = mapped_column()
    rport: Mapped[int] = mapped_column()
    suspended_since: Mapped[datetime | None] = mapped_column()
    created_at: Mapped[CreatedAt]

    keypair_id: Mapped[int] = mapped_column(ForeignKey("agent_keypair.id"))

    keypair: Mapped[AgentKeypair] = relationship()

