import asyncio
import random
import uuid
from enum import Enum
import json
from message_utils import receive

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

        async def run(self) -> None:
            await self.patrol()

        async def patrol(self) -> None:
            if await self.receive_request_clean():
                await self.clean()

            if await self.check_surroundings_for_cleaning():
                await self.clean()

            await self.position_step()
            await asyncio.sleep(1 / 60)

        async def receive_request_clean(self) -> bool:
            msg_body = await receive(behaviour=self, message_type='REQUEST_CLEAN', timeout=0.01)
            if not msg_body: return

            position = Position(
                x=msg_body['payload']['position']['x'], 
                y=msg_body['payload']['position']['y']
            )
            await self.set_state(CleanerAgentStateEnum.DRIVING_TO_DESTINATION)
            await self.drive_to(position)
            return True

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
