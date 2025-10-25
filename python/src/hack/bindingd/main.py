import asyncio

from dishka import make_async_container, Scope, provide, Provider

from hack.core.models.check_implementations.unions import AnyCheckTaskPayload
from hack.core.services.agent import AgentService

from hack.core.providers import ProviderDatabase, ProviderConfig
from hack.core.services.checks import CheckService
from hack.core.services.providers import ProviderServices
from hack.core.services.uow_ctl import UoWCtl
from hack.rest_server.providers import AuthorizedUser


class NoAuthorizedUser(Provider):
    @provide(scope=Scope.APP)
    async def get_authorized_user(self) -> AuthorizedUser:
        return None


providers = [
    ProviderConfig(),
    ProviderDatabase(),
    NoAuthorizedUser(),
    ProviderServices(),
]


async def async_main():
    container = make_async_container(*providers)
    async with container(scope=Scope.SESSION) as app_c:
        while True:
            async with app_c(
                    scope=Scope.REQUEST,
            ) as request_c:
                check_service = await request_c.get(CheckService)
                agent_service = await request_c.get(AgentService)
                check = await check_service.acquire_next_check()
                print(f"Acquired check: {check}")
                if check is None:
                    continue
                async for i in await agent_service.stream_up_ids(limit=10, random_order=True):
                    await check_service.create_check_task(
                        check_uid=check.uid,
                        payload=AnyCheckTaskPayload.validate_python(check.payload),
                        bound_to_agent_id=i,
                    )
                await check_service.ack_check(check_uid=check.uid)
                uow_ctl = await request_c.get(UoWCtl)
                await uow_ctl.commit()

            await asyncio.sleep(0.01)


def main():
    asyncio.run(async_main())
