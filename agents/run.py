import os
import time
from typing import List

from FSMcleaner_agent import CleanerAgent
from guard_agent import GuardAgent
from guide_agent import GuideAgent
from spade.agent import Agent
from ws_connection import get_ws_connection


def create_agents() -> List[Agent]:
    xmpp_server_password = os.environ["XMPP_SERVER_PASSWORD"]
    agents = []

    for i in range(int(os.environ.get("AGENT_CLEANER_NUMBER", 0))):
        xmpp_server_url = f"c{i+1}@{os.environ['XMPP_SERVER_URL']}"
        agents.append(CleanerAgent(xmpp_server_url, xmpp_server_password))

    for i in range(int(os.environ.get("AGENT_GUARD_NUMBER", 0))):
        xmpp_server_url = f"g{i+1}@{os.environ['XMPP_SERVER_URL']}"
        agents.append(GuardAgent(xmpp_server_url, xmpp_server_password))

    for i in range(int(os.environ.get("AGENT_GUIDE_NUMBER", 0))):
        xmpp_server_url = f"k{i+1}@{os.environ['XMPP_SERVER_URL']}"
        agents.append(GuideAgent(xmpp_server_url, xmpp_server_password))

    return agents


def main():
    agents = create_agents()
    for agent in agents:
        future = agent.start()
        future.result()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")

    for agent in agents:
        agent.stop()

    get_ws_connection.close()


if __name__ == "__main__":
    main()
