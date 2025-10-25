from dishka import Provider
from pydantic_settings import BaseSettings, SettingsConfigDict

from hack.core.agent_connector import AgentConnector


class ConfigHack(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_prefix="HACK__AGENT__",
    )


class ProviderAgent(Provider):
    async def provide_agent_config(
            self
    ) -> AgentConnector:
        pass
