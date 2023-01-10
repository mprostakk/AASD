import asyncio
from os import access
import random
import uuid
from enum import Enum
from message_utils import receive

from base_agent import AgentBaseBehaviour
from schemas import AgentEnum, AgentState, Direction, Position
from spade.agent import Agent
from zones_const import PUBLIC_ZONE


class GuideAgentStateEnum(Enum):
    WAITING = "WAITING"
    DRIVING_TO_SOURCE = "DRIVING_TO_SOURCE"
    GUIDING_TO_DESTINATION = "GUIDING_TO_DESTINATION"


class GuideAgentState(AgentState):
    state: GuideAgentStateEnum = GuideAgentStateEnum.WAITING


class GuideAgent(Agent):
    AGENT_NAME = "Guide"

    class GuideBehaviour(AgentBaseBehaviour):
        access = [PUBLIC_ZONE]
        
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
            await self.receive_loss_report()

            source_position = Position(x=random.randint(100, 700), y=random.randint(100, 700))
            destination_position = Position(x=random.randint(100, 700), y=random.randint(100, 700))
            await self.guide(source_position, destination_position)

        async def receive_loss_report(self):
            msg_body = await receive(behaviour=self, message_type='REPORT_LOST', timeout=7)
            if not msg_body: return

            source_position = Position(
                x=msg_body['payload']['source_position']['x'], 
                y=msg_body['payload']['source_position']['y']
            )
            destination_position = Position(
                x=msg_body['payload']['destination_position']['x'], 
                y=msg_body['payload']['destination_position']['y']
            )
            await self.guide(source_position, destination_position)

        async def guide(self, source_position: Position, destination_position: Position):
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
