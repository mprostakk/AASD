from enum import Enum

from schemas import AgentState
from spade.agent import Agent


class GuideAgentStateEnum(Enum):
    ROAMING = "ROAMING"


class GuideAgentState(AgentState):
    state: GuideAgentStateEnum = GuideAgentStateEnum.ROAMING


class GuideAgent(Agent):
    async def run(self):
        pass
