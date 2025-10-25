import asyncio

from dishka import make_async_container, Scope, Provider, provide

from hack.core.models.check_implementations.unions import AnyCheckTaskPayload
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
                # agent_service = await request_c.get(AgentService)
                check_task = await check_service.acquire_next_check_task()
                if check_task is None:
                    continue
                payload = AnyCheckTaskPayload.model_validate(check_task.payload)
                # todo: implement calling remote agents
                result = await payload.perform_check()
                check_task.result = result.model_dump()
                await check_service.store_check_task_result(check_task.uid, result)
                uow_ctl = await request_c.get(UoWCtl)
                await uow_ctl.commit()

            await asyncio.sleep(0.01)


def main():
    asyncio.run(async_main())
