import os
import time

from cleaner_agent import CleanerAgent
from ws_connection import get_ws_connection


def main():
    xmpp_server_url = f"{os.environ['XMPP_SERVER_HOST']}@{os.environ['XMPP_SERVER_URL']}"
    xmpp_server_password = os.environ["XMPP_SERVER_PASSWORD"]
    cleaner_agent = CleanerAgent(xmpp_server_url, xmpp_server_password)

    future = cleaner_agent.start()
    future.result()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")

    cleaner_agent.stop()
    get_ws_connection.close()


if __name__ == "__main__":
    main()
