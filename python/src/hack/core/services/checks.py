from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from hack.core.models.check import Check
from hack.core.models.check_implementations.base import BaseCheckTaskPayload, BaseCheckTaskResult
from hack.core.models.check_task.model import CheckTask


class StreamsServiceError(Exception):
    pass


class StreamNotFoundError(StreamsServiceError):
    pass


class CheckService:
    def __init__(
            self,
            orm_session: AsyncSession,
    ):
        self.orm_session = orm_session

    async def create_check(
            self,
            payload: BaseCheckTaskPayload,
    ) -> Check:
        check = Check(
            payload=payload.model_dump(),
        )
        self.orm_session.add(check)
        await self.orm_session.flush()

        return check

    async def acquire_next_check(
            self,
    ) -> Check | None:
        stmt = (
            select(Check)
            .order_by(Check.created_at.asc())
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        check = await self.orm_session.scalar(stmt)
        return check

    async def create_check_task(
            self,
            check_uid: UUID,
            payload: BaseCheckTaskPayload,
            bound_to_agent_id: int,
    ) -> CheckTask:
        check_task = CheckTask(
            check_uid=check_uid,
            payload=payload.model_dump(),
            result=None,
            bound_to_agent_id=bound_to_agent_id,
        )
        self.orm_session.add(check_task)
        await self.orm_session.flush()
        return check_task

    async def acquire_next_check_task(self) -> CheckTask | None:
        stmt = (
            select(CheckTask)
            .where(CheckTask.acked_at.is_(None))
            .order_by(CheckTask.created_at.asc())
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        check_task = await self.orm_session.scalar(stmt)
        return check_task

    async def get_check_tasks_with(
            self,
            check_uid: UUID,
    ) -> Iterable[CheckTask]:
        stmt = (
            select(CheckTask)
            .where(CheckTask.check_uid.is_(check_uid))
        )
        return await self.orm_session.scalars(stmt)

    async def store_check_task_result(
            self,
            check_uid: UUID,
            result: BaseCheckTaskResult,
    ) -> None:
        stmt = (
            update(CheckTask)
            .where(CheckTask.check_uid.is_(check_uid))
            .values(result=result.model_dump())
        )
        await self.orm_session.execute(stmt)
