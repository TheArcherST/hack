from ipaddress import IPv4Address

import asyncssh
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from hack.core.agent_connector import AgentConnector
from hack.core.models import Agent
from hack.core.models.agent_keypair import AgentKeypair
from hack.rest_server.providers import AuthorizedUser


class AgentService:
    def __init__(
            self,
            orm_session: AsyncSession,
            authorized_user: AuthorizedUser,
    ):
        self.orm_session = orm_session
        self.authorized_user = authorized_user

    async def issue_keypair(
            self,
            passphrase: str | None = None,
    ) -> AgentKeypair:
        # 1) Generate in-memory private key
        algorithm = "ssh-ed25519"
        priv = asyncssh.generate_private_key(algorithm)

        # 2) Export keys as strings (no files)
        pub_line = priv.export_public_key(format_name="openssh")
        pem = priv.export_private_key(passphrase=passphrase)  # OpenSSH new-format PEM

        # 3) Persist to DB
        rec = AgentKeypair(
            name=None,
            algorithm=algorithm,
            public_key_openssh=pub_line.decode("utf-8"),
            private_key_pem=pem,
        )
        self.orm_session.add(rec)
        await self.orm_session.commit()
        await self.orm_session.refresh(rec)
        return rec

    async def get_keypair_with(
            self,
            public_key: str | None = None,
    ) -> AgentKeypair | None:
        stmt = (
            select(AgentKeypair)
            .where(AgentKeypair.public_key_openssh == public_key)
        )
        return await self.orm_session.scalar(stmt)

    async def get_connector(self, agent_id: int) -> AgentConnector:
        agent = await self.orm_session.get(
            Agent, agent_id,
            options=(joinedload(Agent.keypair),),
        )
        return AgentConnector(
            host=agent.ip,
            port=agent.port,
            rhost=agent.rhost,
            rport=agent.rport,
            private_key_pem=agent.keypair.private_key_pem,
        )

    async def create_agent(
            self,
            keypair_id: int,
            ip: IPv4Address,
            port: int,
            rhost: str,
            rport: int,
    ):
        agent = Agent(
            keypair_id=keypair_id,
            ip=str(ip),
            port=port,
            rhost=rhost,
            rport=rport,
            created_by_user=self.authorized_user,
        )
        self.orm_session.add(agent)
        await self.orm_session.flush()

    async def get_agents_with(self):
        stmt = (
            select(Agent)
        )
        return await self.orm_session.execute(stmt)
