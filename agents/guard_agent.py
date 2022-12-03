from enum import Enum

from schemas import AgentState
from spade.agent import Agent


class GuardAgentStateEnum(Enum):
    ROAMING = "ROAMING"


class GuardAgentState(AgentState):
    state: GuardAgentStateEnum = GuardAgentStateEnum.ROAMING


class GuardAgent(Agent):
    async def run(self):
        pass
