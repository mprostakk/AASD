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


class AgentState(BaseModel):
    id: UUID
    type: AgentEnum
    position: Position
