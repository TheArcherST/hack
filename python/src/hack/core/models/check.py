import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from hack.core.models import CheckTask
from hack.core.models.base import Base, CreatedAt


class Check(Base):
    """ Thing that is intended to check if some is operational """

    __tablename__ = "check"

    uid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    payload: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[CreatedAt]

    tasks: Mapped[list[CheckTask]] = relationship(lazy="selectin")
