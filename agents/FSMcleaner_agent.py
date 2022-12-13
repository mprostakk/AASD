import time
import asyncio
import random
import uuid

from spade.agent import Agent
from spade.behaviour import State
from base_agent import AgentBaseBehaviour
from enum import Enum

from spade.message import Message
from message_utils import receive
from schemas import AgentEnum, AgentState, Direction, Position

class CleanerAgentStateEnum(Enum):
    PATROL = "PATROL"
    DRIVING_TO_DESTINATION = "DRIVING_TO_DESTINATION"
    HANDLE_CLEAN = "HANDLE_CLEAN"

class CleanerAgentState(AgentState):
    state: CleanerAgentStateEnum = CleanerAgentStateEnum.PATROL

class CleanerBehaviour(AgentBaseBehaviour):
    async def on_start(self) -> None:
        self.state = CleanerAgentState(
            id=self.agent_id,
            position=Position(x=random.randint(100, 700), y=random.randint(100, 700)),
            type=AgentEnum.CLEANER,
            direction=random.choice(list(Direction)),
        )

class Patrol(State):
    async def run(self):
        if await self.receive_request_clean():
            self.set_next_state(DrivingToDestination)
        if await self.check_surroundings_for_cleaning():
            self.set_next_state(HandleClean)
        await CleanerBehaviour.position_step()
        await self.agent.
        await asyncio.sleep(1 / 60)
    
    async def check_surroundings_for_cleaning(self) -> bool:
            return random.random() < 0.001

    async def receive_request_clean(self):
        msg_body = await receive(behaviour=self, message_type='REQUEST_CLEAN', timeout=0.01)
        if not msg_body: return

        position = Position(
            x=msg_body['payload']['position']['x'], 
            y=msg_body['payload']['position']['y']
        )
        msg_position = Message(to=str(self.agent.jid))
        msg_position.body = position
        await self.send(msg_position)
        return True


class DrivingToDestination(State):
    async def run(self):
        position_msg = await self.receive(timeout=5)
        position = position_msg.body
        await CleanerBehaviour.drive_to(position)
        self.set_next_state(HandleClean)


class HandleClean(State):
    async def run(self):
        await asyncio.sleep(5)
        self.set_next_state(Patrol)



class CleanerAgent(Agent):
    async def setup(self):
        self.agent_id = uuid.uuid4()
        self.state = CleanerAgentState(
                id=self.agent_id,
                position=Position(x=random.randint(100, 700), y=random.randint(100, 700)),
                type=AgentEnum.CLEANER,
                direction=random.choice(list(Direction)),
            )
        fsm = CleanerBehaviour(agent_id=self.agent_id)
        fsm.add_state(name=Patrol, state=Patrol(), initial=True)
        fsm.add_state(name=DrivingToDestination, state=DrivingToDestination())
        fsm.add_state(name=HandleClean, state=HandleClean())
        fsm.add_transition(source=Patrol, dest=DrivingToDestination)
        fsm.add_transition(source=Patrol, dest=HandleClean)
        fsm.add_transition(source=DrivingToDestination, dest=HandleClean)
        fsm.add_transition(source=HandleClean, dest=Patrol)
        self.add_behaviour(fsm)

