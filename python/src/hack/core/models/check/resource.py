from sqlalchemy.orm import mapped_column, Mapped

from ..base import Base


class Resource(Base):
    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(primary_key=True)
    uri: Mapped[str]
