import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Agent
from ..base import Base


class CheckTask(Base):
    __tablename__ = "check_task"

    id: Mapped[int] = mapped_column(primary_key=True)
    check_label: Mapped[UUID] = mapped_column()
    payload: Mapped[dict] = mapped_column(JSON)
    result: Mapped[dict | None] = mapped_column(JSON)
    locked_at: Mapped[datetime | None]
    locked_until: Mapped[datetime | None]
    acked_at: Mapped[datetime | None]

    assigned_agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"))

    agent: Mapped[Agent] = relationship()
