import os
import time

from ws_connection import get_ws_connection
from example_agent import ExampleAgent


def main():
    xmpp_server_url = f"{os.environ['XMPP_SERVER_HOST']}@{os.environ['XMPP_SERVER_URL']}"
    xmpp_server_password = os.environ["XMPP_SERVER_PASSWORD"]
    example_agent = ExampleAgent(xmpp_server_url, xmpp_server_password)

    future = example_agent.start()
    future.result()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")

    example_agent.stop()
    get_ws_connection.close()


if __name__ == "__main__":
    main()
