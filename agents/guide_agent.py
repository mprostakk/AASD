import asyncio
import random
import uuid
from enum import Enum

from base_agent import AgentBaseBehaviour
from schemas import AgentEnum, AgentState, Direction, Position
from spade.agent import Agent


class GuideAgentStateEnum(Enum):
    WAITING = "WAITING"
    DRIVING_TO_SOURCE = "DRIVING_TO_SOURCE"
    GUIDING_TO_DESTINATION = "GUIDING_TO_DESTINATION"


class GuideAgentState(AgentState):
    state: GuideAgentStateEnum = GuideAgentStateEnum.WAITING


class GuideAgent(Agent):
    AGENT_NAME = "Guide"

    class GuideBehaviour(AgentBaseBehaviour):
        async def on_start(self) -> None:
            self.state = GuideAgentState(
                id=self.agent_id,
                position=Position(x=random.randint(100, 700), y=random.randint(100, 700)),
                type=AgentEnum.GUIDE,
                direction=random.choice(list(Direction)),
            )

        async def run(self) -> None:
            await self.patrol()

        async def patrol(self) -> None:
            await self.send_state()
            await asyncio.sleep(7)
            await self.send_state()

            source_position = Position(x=random.randint(100, 700), y=random.randint(100, 700))
            destination_position = Position(x=random.randint(100, 700), y=random.randint(100, 700))

            await self.set_state(GuideAgentStateEnum.DRIVING_TO_SOURCE)
            await self.drive_to(source_position)
            await self.set_state(GuideAgentStateEnum.GUIDING_TO_DESTINATION)
            await asyncio.sleep(1)

            await self.drive_to(destination_position)
            await asyncio.sleep(1)

            await self.set_state(GuideAgentStateEnum.WAITING)

    async def setup(self) -> None:
        self.agent_id = uuid.uuid4()
        print(f"{self.AGENT_NAME} starting with id: {self.agent_id}")
        behave = self.GuideBehaviour(self.agent_id)
        self.add_behaviour(behave)
