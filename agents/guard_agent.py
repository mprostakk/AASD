from enum import Enum

from spade.agent import Agent

from schemas import AgentState


class GuardAgentStateEnum(Enum):
    ROAMING = "ROAMING"


class GuardAgentState(AgentState):
    state: GuardAgentStateEnum = GuardAgentStateEnum.ROAMING


class GuardAgent(Agent):
    async def run(self):
        pass
