import asyncssh
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from hack.agent.connector import AgentConnector
from hack.core.models import Agent
from hack.core.models.agent_keypair import AgentKeypair


class AgentService:
    def __init__(
            self,
            orm_session: AsyncSession,
    ):
        self.orm_session = orm_session

    async def issue_keypair(
            self,
            passphrase: str | None = None,
    ) -> AgentKeypair:
        # 1) Generate in-memory private key
        algorithm = "ssh-ed25519"
        priv = asyncssh.generate_private_key(algorithm)

        # 2) Export keys as strings (no files)
        pub_line = priv.export_public_key()
        pem = priv.export_private_key(passphrase=passphrase)  # OpenSSH new-format PEM

        # 3) Persist to DB
        rec = AgentKeypair(
            name=None,
            algorithm=algorithm,
            public_key_openssh=pub_line,
            private_key_pem=pem,
        )
        self.orm_session.add(rec)
        await self.orm_session.commit()
        await self.orm_session.refresh(rec)
        return rec

    async def get_connector(self, agent_id: int) -> AgentConnector:
        agent = await self.orm_session.get(
            Agent, agent_id,
            options=(joinedload(Agent.keypair),),
        )
        return AgentConnector(
            ssh_host=agent.ip,
            rhost=agent.rhost,
            rport=agent.rport,
            private_key_pem=agent.keypair.private_key_pem,
        )

    async def create_agent(
            self,
            keypair_id: int,
            ip: str,
            rhost: str,
            rport: int,
    ):
        agent = Agent(
            keypair_id=keypair_id,
            ip=ip,
            rhost=rhost,
            rport=rport,

        )

    async def get_agents_with(self):
        stmt = (
            select(Agent)
        )
        return await self.orm_session.execute(stmt)
