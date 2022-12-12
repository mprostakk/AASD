import asyncio
import random
import uuid
from enum import Enum
import os


from base_agent import AgentBaseBehaviour
from schemas import AgentEnum, AgentState, Direction, Position
from spade.agent import Agent
from spade.message import Message
import json
from message_utils import send


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
                position=Position(x=random.randint(100, 700), y=random.randint(100, 700)),
                type=AgentEnum.GUARD,
                direction=random.choice(list(Direction)),
            )

        async def run(self) -> None:
            await self.patrol()

        async def patrol(self) -> None:
            if await self.check_if_area_need_clean(self.state.position):
                await self.send_clean_request(self.state.position)
            
            if await self.check_if_person_need_guide(self.state.position):
                await self.send_report_lost(self.state.position)

            await self.position_step()
            await asyncio.sleep(1 / 60)

        async def check_if_person_need_guide(self, position: Position) -> bool:
            return random.random() < 0.0001

        async def check_if_area_need_clean(self, position: Position) -> bool:
            return random.random() < 0.0005

        async def send_clean_request(self, position: Position) -> None:
            await send(
                behaviour=self, 
                receivers_group="CLEANER",
                receivers_prefix="c",
                message_type="REQUEST_CLEAN", 
                message_payload={ 
                    'position': { 'x': position.x, 'y': position.y }
                }
            )

        async def send_report_lost(self, position: Position) -> None:
            destination_position = Position(x=random.randint(100, 700), y=random.randint(100, 700))
            await send(
                behaviour=self, 
                receivers_group="GUIDE",
                receivers_prefix="k",
                message_type="REPORT_LOST", 
                message_payload={ 
                    'source_position': { 'x': position.x, 'y': position.y },
                    'destination_position': { 'x': destination_position.x, 'y': destination_position.y }
                }
            )
            return



    async def setup(self) -> None:
        self.agent_id = uuid.uuid4()
        print(f"{self.AGENT_NAME} starting with id: {self.agent_id}")
        behave = self.GuardBehaviour(self.agent_id)
        self.add_behaviour(behave)
