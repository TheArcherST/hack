from sqlalchemy.orm import mapped_column, Mapped

from hack.core.models.base import Base


class Resource(Base):
    """
    Resource is something that can be checked; entity that is to be up or down,
    for which check are performed to inspect it's actual state cross Internet.

    """
    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(primary_key=True)
    uri: Mapped[str]
