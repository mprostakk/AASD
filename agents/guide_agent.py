from enum import Enum

from spade.agent import Agent

from schemas import AgentState


class GuideAgentStateEnum(Enum):
    ROAMING = "ROAMING"


class GuideAgentState(AgentState):
    state: GuideAgentStateEnum = GuideAgentStateEnum.ROAMING


class GuideAgent(Agent):
    async def run(self):
        pass
