import asyncio
import uuid
from uuid import UUID

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from schemas import Position, AgentState
from ws_connection import get_ws_connection


class ExampleAgent(Agent):
    class MyBehave(CyclicBehaviour):
        def __init__(self, agent_id: UUID):
            super().__init__()
            self.agent_id = agent_id

        async def on_start(self):
            position = Position(x=0, y=0)
            self.state = AgentState(position=position, id=self.agent_id)

        async def run(self):
            self.state.position.x += 1
            self.state.position.y += 1

            get_ws_connection().send(self.state.json())
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting . . .")
        self.agent_id = uuid.uuid4()
        behave = self.MyBehave(self.agent_id)
        self.add_behaviour(behave)
