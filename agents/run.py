import os
import time

from guide_agent import GuideAgent
from guard_agent import GuardAgent
from cleaner_agent import CleanerAgent
from ws_connection import get_ws_connection


def create_agent():
    xmpp_server_url = f"{os.environ['XMPP_SERVER_HOST']}@{os.environ['XMPP_SERVER_URL']}"
    xmpp_server_password = os.environ["XMPP_SERVER_PASSWORD"]

    agent_type = os.environ['AGENT_TYPE']

    if agent_type == "CLEANER":
        agent = CleanerAgent(xmpp_server_url, xmpp_server_password)
    elif agent_type == "GUARD":
        agent = GuardAgent(xmpp_server_url, xmpp_server_password)
    elif agent_type == "GUIDE":
        agent = GuideAgent(xmpp_server_url, xmpp_server_password)
    else:
        raise NotImplementedError

    return agent


def main():
    agents = []
    agent_number = int(os.environ['AGENT_NUMBER'])
    for x in range(agent_number):
        agent = create_agent()
        agents.append(agent)
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
