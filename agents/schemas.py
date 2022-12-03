from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class AgentEnum(Enum):
    GUARD = "GUARD"
    GUIDE = "GUIDE"
    CLEANER = "CLEANER"


class Position(BaseModel):
    x: int
    y: int


class Direction(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"

    def get_position_to_add(self) -> Position:
        if self == self.UP:
            return Position(x=0, y=3)
        elif self == self.RIGHT:
            return Position(x=3, y=0)
        elif self == self.DOWN:
            return Position(x=0, y=-3)
        else:
            return Position(x=-3, y=0)

    def get_new_direction(self) -> "Direction":
        if self == self.UP:
            return self.RIGHT
        elif self == self.RIGHT:
            return self.DOWN
        elif self == self.DOWN:
            return self.LEFT
        else:
            return self.UP


class AgentState(BaseModel):
    id: UUID
    type: AgentEnum
    position: Position
    direction: Direction
