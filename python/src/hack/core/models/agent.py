from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(unique=True)
    ssh_public_key: Mapped[str] = mapped_column(unique=True)
    # ssh private key is managed by transport microservice
