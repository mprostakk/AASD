import asyncio
import random
import uuid
from enum import Enum

from base_agent import AgentBaseBehaviour
from schemas import AgentEnum, AgentState, Direction, Position
from spade.agent import Agent


class CleanerAgentStateEnum(Enum):
    PATROL = "PATROL"
    DRIVING_TO_DESTINATION = "DRIVING_TO_DESTINATION"
    HANDLE_CLEAN = "HANDLE_CLEAN"


class CleanerAgentState(AgentState):
    state: CleanerAgentStateEnum = CleanerAgentStateEnum.PATROL


class CleanerAgent(Agent):
    AGENT_NAME = "Cleaner"

    class CleanerBehaviour(AgentBaseBehaviour):
        async def on_start(self) -> None:
            self.state = CleanerAgentState(
                id=self.agent_id,
                position=Position(x=random.randint(100, 700), y=random.randint(100, 700)),
                type=AgentEnum.CLEANER,
                direction=random.choice(list(Direction)),
            )

        async def run(self) -> None:
            await self.patrol()

        async def patrol(self) -> None:
            if await self.check_handle_clean_request():
                position = Position(x=100, y=100)
                await self.set_state(CleanerAgentStateEnum.DRIVING_TO_DESTINATION)
                await self.drive_to(position)
                await self.clean()

            if await self.check_surroundings_for_cleaning():
                await self.clean()

            await self.position_step()
            await asyncio.sleep(1 / 60)

        async def check_handle_clean_request(self) -> bool:
            return False

        async def check_surroundings_for_cleaning(self) -> bool:
            return random.random() < 0.001

        async def clean(self) -> None:
            await self.set_state(CleanerAgentStateEnum.HANDLE_CLEAN)
            await asyncio.sleep(5)
            await self.set_state(CleanerAgentStateEnum.PATROL)

    async def setup(self) -> None:
        self.agent_id = uuid.uuid4()
        print(f"{self.AGENT_NAME} starting with id: {self.agent_id}")
        behave = self.CleanerBehaviour(self.agent_id)
        self.add_behaviour(behave)
