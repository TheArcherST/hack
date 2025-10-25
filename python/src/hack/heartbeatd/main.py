from datetime import datetime, timedelta

from dishka import make_async_container, FromDishka
from dishka.integrations.taskiq import inject, setup_dishka, TaskiqProvider
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq.scheduler.scheduled_task import CronSpec
from taskiq_redis import RedisStreamBroker, RedisScheduleSource

from hack.core.models.agent import AgentStatus
from hack.core.providers import ProviderDatabase, ProviderConfig
from hack.core.services.agent import AgentService
from hack.core.services.providers import ProviderServices
from hack.core.services.uow_ctl import UoWCtl
from hack.tasksd.main import NoAuthorizedUser

providers = (
    ProviderConfig(),
    ProviderDatabase(),
    ProviderServices(),
    NoAuthorizedUser(),
    TaskiqProvider(),
)

broker = RedisStreamBroker("redis://redis:6379")
schedule_source = RedisScheduleSource("redis://redis:6379")
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[schedule_source],
)


@broker.task
@inject(patch_module=True)
async def heartbit(
        agent_service: FromDishka[AgentService],
        uow_ctl: FromDishka[UoWCtl],
        agent_id: int,
):
    print("Enter heartbit check")
    connector = await agent_service.get_connector(agent_id)
    async with connector.connect() as conn:
        try:
            await conn.options("/", timeout=2)
            # todo: heartbit endpoint
        except Exception as e:
            print(f"Error while trying to connect to agent {agent_id}: `{e}`")
            status = AgentStatus.DOWN
        else:
            status = AgentStatus.UP
        print(f"Status of agent {agent_id} is set to {status}")
        await agent_service.heartbit_mark(
            agent_id=agent_id,
            status=status,
        )
        await uow_ctl.commit()


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
@inject(patch_module=True)
async def heartbeat_schedule_loop(
        agent_service: FromDishka[AgentService],
):
    print("Enter heartbeat schedule loop")
    async for i in await agent_service.stream_ids():
        for j in range(10):  # 60 seconds / 10 = 6 seconds
            await heartbit.schedule_by_time(
                schedule_source,
                datetime.now() + timedelta(seconds=j * 10),
                agent_id=i,
            )


container = make_async_container(*providers)
setup_dishka(container=container, broker=broker)
