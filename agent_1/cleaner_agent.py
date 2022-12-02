import asyncio
import uuid
from enum import Enum
from uuid import UUID

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
    class MyBehave(CyclicBehaviour):
        def __init__(self, agent_id: UUID):
            super().__init__()
            self.agent_id = agent_id

        async def on_start(self):
            position = Position(x=0, y=0)
            self.state = CleanerAgentState(
                id=self.agent_id, position=position, type=AgentEnum.CLEANER
            )

        async def run(self):
            self.state.position.x += 3
            self.state.position.y += 3

            self.state.position.x %= 500
            self.state.position.y %= 500

            if self.state.position.x < 130:
                self.state.state = CleanerAgentStateEnum.FREE
            elif self.state.position.x < 300:
                self.state.state = CleanerAgentStateEnum.DRIVING_TO_DESTINATION
            else:
                self.state.state = CleanerAgentStateEnum.CLEANING

            get_ws_connection().send(self.state.json())
            await asyncio.sleep(1 / 50)

    async def setup(self):
        print("Agent starting . . .")
        self.agent_id = uuid.uuid4()
        behave = self.MyBehave(self.agent_id)
        self.add_behaviour(behave)
