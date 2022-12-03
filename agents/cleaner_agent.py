import asyncio
import random
import uuid
from enum import Enum
from uuid import UUID

from driving_utils import drive_positions, is_position_on_board
from schemas import AgentEnum, AgentState, Direction, Position
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from ws_connection import get_ws_connection


class CleanerAgentStateEnum(Enum):
    PATROL = "PATROL"
    DRIVING_TO_DESTINATION = "DRIVING_TO_DESTINATION"
    HANDLE_CLEAN = "HANDLE_CLEAN"


class CleanerAgentState(AgentState):
    state: CleanerAgentStateEnum = CleanerAgentStateEnum.PATROL


class CleanerAgent(Agent):
    AGENT_NAME = "Cleaner"

    class MyBehave(CyclicBehaviour):
        def __init__(self, agent_id: UUID):
            super().__init__()
            self.agent_id = agent_id

        async def on_start(self):
            self.state = CleanerAgentState(
                id=self.agent_id,
                position=Position(x=400, y=400),
                type=AgentEnum.CLEANER,
                direction=random.choice(list(Direction)),
            )

        async def set_state(self, state: CleanerAgentStateEnum) -> None:
            self.state.state = state
            await self.send_state()

        async def set_position(self, position: Position) -> None:
            self.state.position = position
            await self.send_state()

        async def drive_to(self, destination: Position):
            await self.set_state(CleanerAgentStateEnum.DRIVING_TO_DESTINATION)
            positions = drive_positions(self.state.position, destination)
            for position in positions:
                await self.set_position(position)
                await asyncio.sleep(1 / 60)

        async def send_state(self):
            get_ws_connection().send(self.state.json())

        async def run(self):
            await self.patrol()

        async def patrol(self):
            if await self.check_handle_clean_request():
                position = Position(x=100, y=100)
                await self.drive_to(position)
                await self.clean()

            if await self.check_surroundings_for_cleaning():
                await self.clean()

            await self.position_step()
            await asyncio.sleep(1 / 60)

        async def position_step(self):
            position_to_add = self.state.direction.get_position_to_add()
            new_position = Position(
                x=self.state.position.x + position_to_add.x,
                y=self.state.position.y + position_to_add.y,
            )
            if is_position_on_board(new_position):
                await self.set_position(new_position)

            if await self.check_if_direction_should_be_changed() or not is_position_on_board(
                new_position
            ):
                self.state.direction = self.state.direction.get_new_direction()

        async def check_handle_clean_request(self) -> bool:
            return False

        async def check_if_direction_should_be_changed(self) -> bool:
            return random.random() < 0.001

        async def check_surroundings_for_cleaning(self) -> bool:
            return random.random() < 0.001

        async def clean(self):
            await self.set_state(CleanerAgentStateEnum.HANDLE_CLEAN)
            await asyncio.sleep(5)
            await self.set_state(CleanerAgentStateEnum.PATROL)

    async def setup(self):
        self.agent_id = uuid.uuid4()
        print(f"{self.AGENT_NAME} starting with id: {self.agent_id}")
        behave = self.MyBehave(self.agent_id)
        self.add_behaviour(behave)
