from datetime import datetime, timedelta
from traceback import print_exception, print_tb
from uuid import UUID

from dishka import make_async_container, FromDishka
from dishka.integrations.taskiq import inject, setup_dishka, TaskiqProvider
from taskiq import TaskiqScheduler, SmartRetryMiddleware, SimpleRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisScheduleSource, ListQueueBroker

from hack.core.models.agent import AgentStatus
from hack.core.models.check_implementations.unions import AnyCheckTaskResult
from hack.core.providers import ProviderDatabase, ProviderConfig
from hack.core.services.agent import AgentService
from hack.core.services.checks import CheckService
from hack.core.services.providers import ProviderServices
from hack.core.services.uow_ctl import UoWCtl
from hack.bindingd.main import NoAuthorizedUser

providers = (
    ProviderConfig(),
    ProviderDatabase(),
    ProviderServices(),
    NoAuthorizedUser(),
    TaskiqProvider(),
)

broker = (ListQueueBroker("redis://redis:6379/1")
          .with_middlewares(SimpleRetryMiddleware(default_retry_count=3)))

non_dynamic_scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])


@broker.task(retry_on_error=True, max_retries=3)
@inject(patch_module=True)
async def process_check_task(
        agent_service: FromDishka[AgentService],
        check_service: FromDishka[CheckService],
        uow_ctl: FromDishka[UoWCtl],
        check_task_uid: UUID,
):
    check_task = await check_service.get_check_task(check_task_uid)
    connector = await agent_service.get_connector(agent_id=check_task.bound_to_agent_id)

    e = None
    try:
        async with connector.connect() as conn:
            json_data = {"payload": check_task.payload}
            response = await conn.post("/check", json=json_data, timeout=40)
    except TimeoutError as e:
        print(f"Timeout error for agent {check_task.bound_to_agent_id}")
        await check_service.notify_check_task_failed(check_task.uid)
    except Exception as e:
        print(f"Some unknown error for agent {check_task.bound_to_agent_id}: `{e}`")
        print_exception(e)
        await check_service.notify_check_task_failed(check_task.uid)
    else:
        if not response.is_success:
            print(f"Some problem on agent's {check_task.bound_to_agent_id} side: code `{response.status_code}`")
            await check_service.notify_check_task_failed(check_task.uid)
        else:
            result = AnyCheckTaskResult.validate_python(response.json())
            print(f"Store result: {result}")
            await check_service.store_check_task_result(check_task.uid, result)
    await uow_ctl.commit()

    if e is not None:
        raise RuntimeError("Retry?") from e

    return None


container = make_async_container(*providers)
setup_dishka(container=container, broker=broker)
