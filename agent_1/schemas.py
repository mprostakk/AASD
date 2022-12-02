from uuid import UUID

from pydantic import BaseModel


class Position(BaseModel):
    x: int
    y: int


class AgentState(BaseModel):
    position: Position
    id: UUID
