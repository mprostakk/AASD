import asyncio
import random
import uuid
from enum import Enum

from base_agent import AgentBaseBehaviour
from schemas import AgentEnum, AgentState, Direction, Position
from spade.agent import Agent


class GuardAgentStateEnum(Enum):
    PATROL = "PATROL"


class GuardAgentState(AgentState):
    state: GuardAgentStateEnum = GuardAgentStateEnum.PATROL


class GuardAgent(Agent):
    AGENT_NAME = "Guard"

    class GuardBehaviour(AgentBaseBehaviour):
        async def on_start(self) -> None:
            self.state = GuardAgentState(
                id=self.agent_id,
                position=Position(x=400, y=400),
                type=AgentEnum.GUARD,
                direction=random.choice(list(Direction)),
            )

        async def run(self) -> None:
            await self.patrol()

        async def patrol(self) -> None:
            await self.position_step()
            await asyncio.sleep(1 / 60)

    async def setup(self) -> None:
        self.agent_id = uuid.uuid4()
        print(f"{self.AGENT_NAME} starting with id: {self.agent_id}")
        behave = self.GuardBehaviour(self.agent_id)
        self.add_behaviour(behave)
