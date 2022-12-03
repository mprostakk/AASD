import asyncio
import random
import uuid
from enum import Enum
from uuid import UUID

from driving_utils import drive_positions
from schemas import AgentEnum, AgentState, Position
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from ws_connection import get_ws_connection


class CleanerAgentStateEnum(Enum):
    FREE = "FREE"
    DRIVING_TO_DESTINATION = "DRIVING_TO_DESTINATION"
    CLEANING = "CLEANING"


class CleanerAgentState(AgentState):
    state: CleanerAgentStateEnum = CleanerAgentStateEnum.FREE


class CleanerAgent(Agent):
    AGENT_NAME = "Cleaner"

    class MyBehave(CyclicBehaviour):
        def __init__(self, agent_id: UUID):
            super().__init__()
            self.agent_id = agent_id

        async def on_start(self):
            self.state = CleanerAgentState(
                id=self.agent_id,
                position=Position(x=0, y=0),
                type=AgentEnum.CLEANER
            )

        async def drive_to(self, destination: Position):
            positions = drive_positions(self.state.position, destination)
            for position in positions:
                get_ws_connection().send(self.state.json())
                self.state.position = position
                await asyncio.sleep(1 / 60)

        async def run(self):
            corners = [
                Position(x=100, y=100),
                Position(x=1000, y=1000),
                Position(x=1000, y=100),
                Position(x=1000, y=1000),
                Position(x=100, y=100),
                Position(x=1000, y=1000),
                Position(x=100, y=1000),
                Position(x=1000, y=1000),
            ]

            random.shuffle(corners)

            for corner in corners:
                await self.drive_to(corner)

    async def setup(self):
        self.agent_id = uuid.uuid4()
        print(f"{self.AGENT_NAME} starting with id: {self.agent_id}")
        behave = self.MyBehave(self.agent_id)
        self.add_behaviour(behave)
