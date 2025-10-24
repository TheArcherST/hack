from datetime import datetime

from sqlalchemy import JSON
from sqlalchemy.orm import mapped_column, Mapped

from hack.core.models.base import Base


class Check(Base):
    __tablename__ = "check"

    id: Mapped[int] = mapped_column(primary_key=True)
    payload: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column()
