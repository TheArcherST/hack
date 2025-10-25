from collections.abc import Iterable
from typing import Any, Literal

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from hack.core.models.check import Check
from hack.server.providers import AuthorizedUser


class StreamsServiceError(Exception):
    pass


class StreamNotFoundError(StreamsServiceError):
    pass


class CheckService:
    def __init__(
            self,
            orm_session: AsyncSession,
            authorized_user: AuthorizedUser,
    ):
        self.orm_session = orm_session
        self.authorized_user = authorized_user

    async def create_check(
            self,
    ) -> Check:
        check = Check(

        )
        stream = Stream(
            name=name,
            json_schema=json_schema,
            created_by_user_id=self.authorized_user.id,
            is_private=is_private,
            record_intent=RecordIntent(
                ttl=None,
                errata_allowed=True,
            ),
        )
        self.orm_session.add(stream)
        await self.orm_session.flush()

        return stream

    def _accessible_streams_stmt(self):
        stmt = (select(Stream)
                .where(
                    or_(Stream.created_by_user_id == self.authorized_user.id,
                        Stream.is_private.is_(False)))
                )
        return stmt

    async def get_checks(
            self,
    ) -> Iterable[Check]:
        stmt = self._accessible_streams_stmt()
        return await self.orm_session.scalars(stmt)

    async def get_check_with(
            self,
            id_: int | None = None,
            name: str | None = None,
    ) -> Check | None:
        stmt = self._accessible_streams_stmt()

        if id_ is not None:
            stmt = stmt.where(Stream.id == id_)
        if name is not None:
            stmt = stmt.where(Stream.name == name)

        stream = await self.orm_session.scalar(stmt)
        return stream
