import asyncio
import random
from uuid import UUID

from driving_utils import drive_positions, is_position_on_board
from schemas import Position
from spade.behaviour import CyclicBehaviour
from ws_connection import get_ws_connection


class AgentBaseBehaviour(CyclicBehaviour):
    def __init__(self, agent_id: UUID):
        super().__init__()
        self.agent_id = agent_id
        self.state = None

    async def set_state(self, state) -> None:
        self.state.state = state
        await self.send_state()

    async def set_position(self, position: Position) -> None:
        self.state.position = position
        await self.send_state()

    async def send_state(self):
        get_ws_connection().send(self.state.json())

    async def drive_to(self, destination: Position):
        positions = drive_positions(self.state.position, destination)
        for position in positions:
            await self.set_position(position)
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

    async def check_if_direction_should_be_changed(self) -> bool:
        return random.random() < 0.001
