from datetime import datetime

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from hack.core.models.base import Base, CreatedAt


class Check(Base):
    """ Thing that is intended to check if some is operational """

    __tablename__ = "check"

    id: Mapped[int] = mapped_column(primary_key=True)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[CreatedAt]
